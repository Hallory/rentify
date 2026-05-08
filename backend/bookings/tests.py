from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from bookings.models import Booking
from properties.models import Property
from users.models import User


class BookingPermissionTests(APITestCase):
    def setUp(self):
        self.tenant = User.objects.create_user(
            email="tenant@test.com",
            username="tenant",
            password="password123",
            role=User.Roles.TENANT,
        )

        self.other_tenant = User.objects.create_user(
            email="other_tenant@test.com",
            username="other_tenant",
            password="password123",
            role=User.Roles.TENANT,
        )

        self.landlord = User.objects.create_user(
            email="landlord@test.com",
            username="landlord",
            password="password123",
            role=User.Roles.LANDLORD,
        )

        self.property = Property.objects.create(
            owner=self.landlord,
            title="Berlin Studio",
            description="Nice studio in Berlin",
            property_type=Property.PropertyType.STUDIO,
            deal_type=Property.DealType.RENT,
            guests=2,
            rooms=1,
            bedrooms=1,
            bathrooms=1,
            area_sqm=35,
            price_per_night=Decimal("90.00"),
            address="Teststrasse 1",
            country="Germany",
            city="Berlin",
            district="Mitte",
            zip_code="10115",
            status=Property.Status.PUBLISHED,
        )

        self.booking = Booking.objects.create(
            user=self.tenant,
            rental_property=self.property,
            check_in=timezone.localdate() + timedelta(days=10),
            check_out=timezone.localdate() + timedelta(days=13),
            guests=2,
            price_per_night_snapshot=self.property.price_per_night,
            total_price=self.property.price_per_night * Decimal("3"),
            status=Booking.Status.PENDING,
        )

    def test_tenant_can_see_own_booking(self):
        self.client.force_authenticate(user=self.tenant)

        response = self.client.get("/api/bookings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.booking.id)

    def test_other_tenant_cannot_see_booking(self):
        self.client.force_authenticate(user=self.other_tenant)

        response = self.client.get("/api/bookings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_landlord_can_see_booking_for_own_property(self):
        self.client.force_authenticate(user=self.landlord)

        response = self.client.get("/api/bookings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.booking.id)
        
        
    def test_tenant_can_cancel_own_booking(self):
        self.client.force_authenticate(user=self.tenant)

        response = self.client.patch(f"/api/bookings/{self.booking.id}/cancel/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.CANCELLED)
        self.assertIsNotNone(self.booking.cancelled_at)
        
    
    def test_landlord_can_confirm_for_own_property(self):
        self.client.force_authenticate(user=self.landlord)

        response = self.client.patch(f"/api/bookings/{self.booking.id}/confirm/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.CONFIRMED)
        
        
    def test_tenant_cannot_confirm_booking(self):
        self.client.force_authenticate(user=self.tenant)

        response = self.client.patch(f"/api/bookings/{self.booking.id}/confirm/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.PENDING)
