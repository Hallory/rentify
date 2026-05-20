from rest_framework import mixins, permissions, viewsets

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Favorite.objects.all()
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related(
            "user", "rental_property"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
