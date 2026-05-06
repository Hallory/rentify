from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Favorite
        fields = [
            'id',
            'user',
            'rental_property',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'created_at',
        ]