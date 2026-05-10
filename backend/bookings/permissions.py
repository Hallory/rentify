from properties.models import Property
from rest_framework import permissions


class OwnerCantBookingPermissions(permissions.BasePermission):
    message = "You cannot book your own property."

    def has_permission(self, request, view):
        if view.action != "create":
            return True

        rental_property_id = request.data.get("rental_property")
        if not rental_property_id:
            return True

        try:
            rental_property = Property.objects.get(id=rental_property_id)
        except Property.DoesNotExist:
            return True

        return request.user.is_authenticated and rental_property.owner != request.user
