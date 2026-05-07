from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Property


class PpopertyPermissionTests(APITestCase):
    def setUp(self):
        self.tenant = User.objects.create_user(
            email="tenant@test.com",
            username="tenant",
            password="password123",
            role=User.Roles.TENANT,
        )
        self.landlord = User.objects.create_user(
            email="landlord@test.com",
            username="landlord",
            password="password123",
            role=User.Roles.LANDLORD,
        )

        self.payload = {
            "title": "Berlin Studio",
            "description": "Nice studio in Berlin",
            "property_type": Property.PropertyType.STUDIO,
            "deal_type": Property.DealType.RENT,
            "guests": 2,
            "rooms": 1,
            "bedrooms": 1,
            "bathrooms": 1,
            "area_sqm": 35,
            "price_per_night": "90.00",
            "address": "Teststrasse 1",
            "country": "Germany",
            "city": "Berlin",
            "district": "Mitte",
            "zip_code": "10115",
            "status": Property.Status.PUBLISHED,
            "amenities": [],
        }

        self.property = Property.objects.create(
            owner=self.landlord,
            title="Original Title",
            description="Original Description",
            property_type=Property.PropertyType.STUDIO,
            deal_type=Property.DealType.RENT,
            guests=2,
            rooms=1,
            bedrooms=1,
            bathrooms=1,
            area_sqm=35,
            price_per_night="90.00",
            address="Teststrasse 1",
            country="Germany",
            city="Berlin",
            district="Mitte",
            zip_code="10115",
            status=Property.Status.PUBLISHED,
        )

        self.other_landlord = User.objects.create_user(
            email="other_landlord@test.com",
            username="other_landlord",
            password="password123",
            role=User.Roles.LANDLORD,
        )

    def test_tenant_cannot_create_property(self):
        self.client.force_authenticate(user=self.tenant)

        response = self.client.post("/api/properties/", self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_landlord_can_create_property(self):
        self.client.force_authenticate(user=self.landlord)

        response = self.client.post("/api/properties/", self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["owner"], self.landlord.id)

    def test_owner_can_update_property(self):
        self.client.force_authenticate(user=self.landlord)

        response = self.client.patch(
            f"/api/properties/{self.property.id}/",
            {"title": "Updated Title"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.property.refresh_from_db()
        self.assertEqual(self.property.title, "Updated Title")

    def test_non_owner_cannot_update_property(self):
        self.client.force_authenticate(user=self.other_landlord)

        response = self.client.patch(
            f"/api/properties/{self.property.id}/", self.payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.property.refresh_from_db()
        self.assertEqual(self.property.title, "Original Title")
