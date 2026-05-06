from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import re

from .serializers import PropertySerializer
from .models import Property
from .filters import PropertyFilter
from analytics.models import SearchHistory


def normalize_query(value):
    normalized_query = re.sub(r'\s+', ' ', value.strip().lower())
    return normalized_query


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'city', 'district']
    ordering_fields = ['price_per_night', 'created_at', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset =  Property.objects.select_related('owner').prefetch_related('amenities')
        
        if self.request.method in permissions.SAFE_METHODS:
            return queryset.filter(status=Property.Status.PUBLISHED)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
            
            
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        raw_query = request.query_params.get('search', '')
        normalized_query = normalize_query(raw_query)
        
        if normalized_query:
            try:
                SearchHistory.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    query=raw_query,
                    normalized_query=normalized_query,
                    city=request.query_params.get('city', ''),
                    property_type=request.query_params.get('property_type', ''),
                    price_min=request.query_params.get('price_min') or None,
                    price_max=request.query_params.get('price_max') or None,
                    rooms_min=request.query_params.get('rooms_min') or None,
                    rooms_max=request.query_params.get('rooms_max') or None,
                    results_count=response.data.get('count', 0),
                )
            except Exception:
                pass
            
        return response