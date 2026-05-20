from django.utils import timezone
from bookings.models import Booking
from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.id")
    rental_property = serializers.ReadOnlyField(source="rental_property.id")

    class Meta:
        model = Review
        fields = [
            "id",
            "author",
            "rental_property",
            "booking",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "author",
            "rental_property",
            "created_at",
            "updated_at",
        ]

    def validate_booking(self, booking):
        request = self.context.get("request")

        if request is None or request.user.is_anonymous:
            raise serializers.ValidationError("User is not authenticated.")

        if booking.user != request.user:
            raise serializers.ValidationError("You can only review your own bookings.")

        if booking.rental_property.owner == request.user:
            raise serializers.ValidationError("You cannot review your own property.")

        today = timezone.localdate()
        if booking.status == Booking.Status.CONFIRMED and booking.check_out < today:
            booking.status = Booking.Status.COMPLETED
            booking.save(update_fields=["status", "updated_at"])

        if booking.status != Booking.Status.COMPLETED:
            raise serializers.ValidationError(
                "Only completed bookings can be reviewed."
            )

        return booking

    def create(self, validated_data):
        booking = validated_data["booking"]
        validated_data["rental_property"] = booking.rental_property
        validated_data["author"] = self.context["request"].user

        return super().create(validated_data)
