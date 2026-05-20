from rest_framework import serializers

from properties.serializers import PropertySerializer
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    rental_property_detail = PropertySerializer(source="rental_property", read_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        rental_property = attrs.get("rental_property")

        if (
            request
            and request.user.is_authenticated
            and Favorite.objects.filter(
                user=request.user, rental_property=rental_property
            ).exists()
        ):
            raise serializers.ValidationError(
                "You have already favorited this property."
            )

        return attrs

    class Meta:
        model = Favorite
        fields = [
            "id",
            "user",
            "rental_property",
            "rental_property_detail",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "rental_property_detail",
            "created_at",
        ]
