from rest_framework import viewsets, permissions

from .serializers import PropertySerializer
from .models import Property


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset =  Property.objects.select_related('owner').prefetch_related('amenities')
        
        if self.request.method in permissions.SAFE_METHODS:
            return queryset.filter(status=Property.Status.PUBLISHED)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
            
            