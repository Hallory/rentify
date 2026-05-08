from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

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
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]
