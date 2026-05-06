from rest_framework import serializers

from .models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = [
            "id",
            "user",
            "query",
            "normalized_query",
            "city",
            "property_type",
            "price_min",
            "price_max",
            "rooms_min",
            "rooms_max",
            "results_count",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "normalized_query",
            "results_count",
            "created_at",
        ]
