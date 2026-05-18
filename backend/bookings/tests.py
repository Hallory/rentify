from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from properties.models import Property
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

from bookings.models import Booking


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

    def test_user_cannot_create_overlapping_booking(self):
        self.client.force_authenticate(user=self.other_tenant)

        response = self.client.post(
            "/api/bookings/",
            {
                "rental_property": self.property.id,
                "check_in": timezone.localdate() + timedelta(days=11),
                "check_out": timezone.localdate() + timedelta(days=14),
                "guests": 2,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_landlord_can_book_other_landlords_property(self):
        other_landlord = User.objects.create_user(
            email="other_landlord@test.com",
            username="other_landlord",
            password="password123",
            role=User.Roles.LANDLORD,
        )

        other_property = Property.objects.create(
            owner=other_landlord,
            title="Munich Apartment",
            description="Nice apartment in Munich",
            property_type=Property.PropertyType.STUDIO,
            deal_type=Property.DealType.RENT,
            guests=2,
            rooms=1,
            bedrooms=1,
            bathrooms=1,
            area_sqm=35,
            price_per_night=Decimal("120.00"),
            address="Teststrasse 2",
            country="Germany",
            city="Munich",
            district="Center",
            zip_code="80331",
            status=Property.Status.PUBLISHED,
        )

        self.client.force_authenticate(user=self.landlord)

        response = self.client.post(
            "/api/bookings/",
            {
                "rental_property": other_property.id,
                "check_in": timezone.localdate() + timedelta(days=11),
                "check_out": timezone.localdate() + timedelta(days=14),
                "guests": 2,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_landlord_can_complete_confirmed_booking(self):
        self.booking.status = Booking.Status.CONFIRMED
        self.booking.save(update_fields=["status"])

        self.client.force_authenticate(user=self.landlord)

        response = self.client.patch(f"/api/bookings/{self.booking.id}/complete/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.COMPLETED)

    def test_tenant_cannot_complete_booking(self):
        self.booking.status = Booking.Status.CONFIRMED
        self.booking.save(update_fields=["status"])

        self.client.force_authenticate(user=self.tenant)

        response = self.client.patch(f"/api/bookings/{self.booking.id}/complete/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.CONFIRMED)

    def test_user_can_create_back_to_back_booking(self):
        self.client.force_authenticate(user=self.other_tenant)

        response = self.client.post(
            "/api/bookings/",
            {
                "rental_property": self.property.id,
                "check_in": self.booking.check_out,
                "check_out": self.booking.check_out + timedelta(days=2),
                "guests": 2,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tenant_cannot_cancel_booking_within_three_days_of_check_in(self):
        self.booking.check_in = timezone.localdate() + timedelta(days=3)
        self.booking.check_out = timezone.localdate() + timedelta(days=6)
        self.booking.save(update_fields=["check_in", "check_out"])

        self.client.force_authenticate(user=self.tenant)

        response = self.client.patch(f"/api/bookings/{self.booking.id}/cancel/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.PENDING)
        self.assertIsNone(self.booking.cancelled_at)

    def test_tenant_can_cancel_booking_more_than_three_days_before_check_in(self):
        self.booking.check_in = timezone.localdate() + timedelta(days=4)
        self.booking.check_out = timezone.localdate() + timedelta(days=7)
        self.booking.save(update_fields=["check_in", "check_out"])

        self.client.force_authenticate(user=self.tenant)

        response = self.client.patch(f"/api/bookings/{self.booking.id}/cancel/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.Status.CANCELLED)
        self.assertIsNotNone(self.booking.cancelled_at)
