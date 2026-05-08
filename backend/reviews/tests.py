from rest_framework import status
from rest_framework.test import APITestCase

from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

from .models import Review
from bookings.models import Booking
from properties.models import Property
from users.models import User


class ReviewPermissionTests(APITestCase):
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
            guests=2,
            price_per_night_snapshot=Decimal("90.00"),
            total_price=Decimal("450.00"),
            check_in=timezone.localdate() + timedelta(days=10),
            check_out=timezone.localdate() + timedelta(days=13),
            status=Booking.Status.CONFIRMED,
        )
        
        self.review = Review.objects.create(
            author=self.tenant,
            rental_property=self.property,
            booking=self.booking,
            rating=4,
            comment="Great property!",
        )
        
        self.booking_without_review = Booking.objects.create(
            user=self.tenant,
            rental_property=self.property,
            guests=2,
            price_per_night_snapshot=Decimal("90.00"),
            total_price=Decimal("450.00"),
            check_in=timezone.localdate() + timedelta(days=10),
            check_out=timezone.localdate() + timedelta(days=13),
            status=Booking.Status.CONFIRMED,
        )
        
        self.other_booking = Booking.objects.create(
            user=self.other_tenant,
            rental_property=self.property,
            guests=2,
            price_per_night_snapshot=Decimal("90.00"),
            total_price=Decimal("270.00"),
            check_in=timezone.localdate() + timedelta(days=30),
            check_out=timezone.localdate() + timedelta(days=33),
            status=Booking.Status.CONFIRMED,
        )
        
    def test_anonymous_can_read_reviews(self):
        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        
        
    def test_user_can_create_review_for_own_confirmed_booking(self):
        self.client.force_authenticate(user=self.tenant)
        
        response = self.client.post("/api/reviews/", {"booking": self.booking_without_review.id, "rating": 5, "comment": "Great property!"}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], self.tenant.id)
        self.assertEqual(response.data["rental_property"], self.property.id)
        self.assertEqual(response.data["booking"], self.booking_without_review.id)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["comment"], "Great property!")

        
    def test_user_cannot_create_review_for_another_users_booking(self):
        self.client.force_authenticate(user=self.tenant)
        
        response = self.client.post("/api/reviews/", {"booking": self.other_booking.id, "rating": 5, "comment": "Great property!"}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_author_can_update_review(self):
        self.client.force_authenticate(user=self.tenant)
        
        response = self.client.patch(f"/api/reviews/{self.review.id}/", {"rating": 5, "comment": "Updated comment!"}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author"], self.tenant.id)
        self.assertEqual(response.data["rental_property"], self.property.id)
        self.assertEqual(response.data["booking"], self.booking.id)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["comment"], "Updated comment!")
        
        
    def test_non_author_cannot_update_review(self):
        self.client.force_authenticate(user=self.other_tenant)
        
        response = self.client.patch(f"/api/reviews/{self.review.id}/", {"rating": 5, "comment": "Updated comment!"}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)