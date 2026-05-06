from django.db.models import Count
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import SearchHistory
from .serializers import SearchHistorySerializer


class SearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def popular(self, request):
        popular_queries = (
            SearchHistory.objects.exclude(normilized_query="")
            .values("normalized_query")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        
        return Response([
            {
                "query": item["normalized_query"],
                "count": item["count"],
            }
            for item in popular_queries
        ])
