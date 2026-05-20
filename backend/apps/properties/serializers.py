from rest_framework import serializers

from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ["owner", "created_at", "updated_at", "views_count"]


class PropertySearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=500)
