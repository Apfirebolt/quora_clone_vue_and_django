"""
Tests for the Question API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from api.serializers import TagSerializer
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag


TAG_URL = reverse('api:tags')


def detail_url(tag_id):
    """Return tag detail URL"""
    return reverse('api:tag-detail', args=[tag_id])


class PublicTagApiTests(TestCase):
    """Test the publicly available tag API"""

    def setUp(self):
        self.client = APIClient()


class PrivateTagApiTests(TestCase):
    """Test the authorized user Tag API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    
    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        res = self.client.post(TAG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_delete_tag(self):
        """Test deleting a tag"""
        tag = Tag.objects.create(name='Test tag')
        url = detail_url(tag.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


    def test_update_tag(self):
        """Test updating a tag"""
        tag = Tag.objects.create(name='Test tag')
        payload = {'name': 'Updated tag'}
        url = detail_url(tag.id)
        self.client.patch(url, payload)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])


       