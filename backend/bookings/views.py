from django.db.models import Q
from django.utils import timezone
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Booking
from .permissions import OwnerCantBookingPermissions
from .serializers import BookingSerializer


class BookingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerCantBookingPermissions]
    queryset = Booking.objects.all()

    def get_queryset(self):
        user = self.request.user

        return Booking.objects.filter(
            Q(user=user) | Q(rental_property__owner=user)
        ).select_related("rental_property", "user")

    @action(detail=True, methods=["patch"])
    def confirm(self, request, pk=None):
        booking = self.get_object()

        if booking.rental_property.owner != request.user:
            return Response(
                {"detail": "Only property owners can confirm bookings."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if booking.status != Booking.Status.PENDING:
            return Response(
                {"detail": "Only pending bookings can be confirmed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.CONFIRMED
        booking.save(update_fields=["status", "updated_at"])

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    def reject(self, request, pk=None):
        booking = self.get_object()

        if booking.rental_property.owner != request.user:
            return Response(
                {"detail": "Only property owners can reject bookings."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if booking.status != Booking.Status.PENDING:
            return Response(
                {"detail": "Only pending bookings can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.REJECTED
        booking.save(update_fields=["status", "updated_at"])

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.user != request.user:
            return Response(
                {"detail": "Only booking owners can cancel bookings."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if booking.status not in [Booking.Status.PENDING, Booking.Status.CONFIRMED]:
            return Response(
                {"detail": "Only pending bookings can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.CANCELLED
        booking.cancelled_at = timezone.now()
        booking.save(update_fields=["status", "cancelled_at", "updated_at"])

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
