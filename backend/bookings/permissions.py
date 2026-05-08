from properties.models import Property
from rest_framework import permissions


class OwnerCantBookingPermissions(permissions.BasePermission):
    message = "You cannot book your own property."

    def has_permission(self, request, view):
        property = Property.objects.get(pk=request.data["rental_property"])
        return (
            request.user
            and request.user.is_authenticated
            and request.user != property.owner
        )
