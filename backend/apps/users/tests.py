from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
            username="user",
            role=User.Roles.TENANT,
        )

    def test_user_cannot_change_role_from_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            "/api/users/me/", {"role": User.Roles.LANDLORD}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.role, User.Roles.TENANT)
        self.assertEqual(response.data['role'], User.Roles.TENANT)
