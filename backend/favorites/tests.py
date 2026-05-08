from properties.models import Property
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

from .models import Favorite


class FavoritePermissionsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
            username="user",
            role=User.Roles.TENANT,
        )
        self.other_user = User.objects.create_user(
            email="other_user@test.com",
            password="password123",
            username="other_user",
            role=User.Roles.TENANT,
        )
        self.landlord = User.objects.create_user(
            email="landlord@test.com",
            password="password123",
            username="landlord",
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
            price_per_night="90.00",
            address="Teststrasse 1",
            country="Germany",
            city="Berlin",
            district="Mitte",
            zip_code="10115",
            status=Property.Status.PUBLISHED,
        )

    def test_unautenticated_user_access_favorite(self):
        response = self.client.get("/api/favorites/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_add_favorite(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/favorites/", {"rental_property": self.property.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.count(), 1)
        self.assertEqual(Favorite.objects.first().user, self.user)

    def test_user_can_sees_only_own_favorites(self):
        Favorite.objects.create(user=self.other_user, rental_property=self.property)

        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/favorites/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_duplicate_favorite_is_rejected(self):
        Favorite.objects.create(user=self.user, rental_property=self.property)

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/favorites/", {"rental_property": self.property.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
