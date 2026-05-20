from properties.models import Property
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

from .models import PropertyView, SearchHistory


class AnalyticsTests(APITestCase):
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
            price_per_night="120.00",
            address="Teststrasse 2",
            country="Germany",
            city="Berlin",
            district="Mitte",
            zip_code="12345",
            status=Property.Status.PUBLISHED,
        )

    def test_property_search_creates_search_history(self):
        self.client.force_authenticate(user=self.tenant)

        response = self.client.get("/api/properties/?search=berlin")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SearchHistory.objects.count(), 1)

        search = SearchHistory.objects.first()
        self.assertEqual(search.user, self.tenant)
        self.assertEqual(search.query, "berlin")
        self.assertEqual(search.normalized_query, "berlin")
        self.assertEqual(search.results_count, 1)

    def test_user_can_see_only_own_searrch_history(self):
        SearchHistory.objects.create(
            user=self.tenant,
            query="berlin",
            normalized_query="berlin",
            results_count=1,
        )
        SearchHistory.objects.create(
            user=self.other_tenant,
            query="munich",
            normalized_query="munich",
            results_count=1,
        )

        self.client.force_authenticate(user=self.tenant)

        response = self.client.get("/api/search-history/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["query"], "berlin")

    def test_property_view_increments_view_count_once_per_user_per_day(self):
        self.client.force_authenticate(user=self.tenant)

        first_response = self.client.get(f"/api/properties/{self.property.id}/")
        second_response = self.client.get(f"/api/properties/{self.property.id}/")

        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)

        self.property.refresh_from_db()
        self.assertEqual(self.property.views_count, 1)
        self.assertEqual(PropertyView.objects.count(), 1)

    def test_owner_view_does_not_increment_views_count(self):
        self.client.force_authenticate(user=self.landlord)

        response = self.client.get(f"/api/properties/{self.property.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.property.refresh_from_db()
        self.assertEqual(self.property.views_count, 0)
        self.assertEqual(PropertyView.objects.count(), 0)
