"""
Tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("api:signup")
TOKEN_URL = reverse("api:signin")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def user_detail_url(username):
    """Return user detail URL."""
    return reverse("api:user-detail", args=[username])

def user_profile_url():
    """Return user profile URL."""
    return reverse("api:profile")

def user_follow_url(username):
    """Return user follow URL."""
    return reverse("api:follow", args=[username])

def user_change_password_url():
    """Return user change password URL."""
    return reverse("api:change-password")


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "username": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "username": "Test Name",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "username": "Test name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            "username": "Test Name",
            "email": "test@example.com",
            "password": "test-user-password123",
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("refresh", res.data)
        self.assertIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email="test@example.com", password="goodpass")

        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {"email": "test@example.com", "password": "pass123"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile_unauthorized(self):
        """Test that profile is not accessible without authentication."""
        self.client.force_authenticate(user=None)
        res = self.client.get(user_profile_url())

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email="test@example.com",
            password="testpass123",
            username="Test Name",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    
    def test_get_user_detail(self):
        """Test retrieving user detail for authenticated user."""
        res = self.client.get(user_detail_url(self.user.username))

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_get_profile_success(self):
        """Test getting profile for authenticated user."""
        res = self.client.get(user_profile_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "username": self.user.username,
            "email": self.user.email,
            "id": self.user.id,
            "firstName": self.user.firstName,
            "lastName": self.user.lastName,
        })

    def test_follow_user(self):
        """Test following a user."""
        user2 = create_user(
            email="testemail2@gmail.com", password="testpass123", username="Test Name 2"
        )
        url = user_follow_url(user2.username)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        

    def test_unfollow_user(self):
        """Test unfollowing a user."""
        user2 = create_user(
            email="testemail2@gmail.com", password="testpass123", username="Test Name 2"
        )
        url = user_follow_url(user2.username)
        self.client.post(url)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_change_password(self):
        """Test changing user password."""
        payload = {
            "current_password": "testpass123",
            "new_password": "newpass123",
        }
        res = self.client.put(user_change_password_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload["new_password"]))
        self.assertFalse(self.user.check_password(payload["current_password"]))
