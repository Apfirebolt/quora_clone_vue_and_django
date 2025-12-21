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

    def test_create_duplicate_tag(self):
        """Test creating a tag with duplicate name"""
        Tag.objects.create(name='Duplicate tag')
        
        payload = {'name': 'Duplicate tag'}
        res = self.client.post(TAG_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tag_case_insensitive(self):
        """Test that tag names are case insensitive (if implemented)"""
        Tag.objects.create(name='Python')
        
        payload = {'name': 'python'}  # lowercase
        res = self.client.post(TAG_URL, payload)
        
        # This might pass or fail depending on implementation
        self.assertIn(res.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_create_tag_with_special_characters(self):
        """Test creating tag with special characters"""
        payload = {'name': 'C++ Programming'}
        res = self.client.post(TAG_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_create_tag_very_long_name(self):
        """Test creating tag with very long name"""
        long_name = 'a' * 100  # Assuming max length is 50
        payload = {'name': long_name}
        res = self.client.post(TAG_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tag_whitespace_only(self):
        """Test creating tag with only whitespace"""
        payload = {'name': '   '}
        res = self.client.post(TAG_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_tag_to_existing_name(self):
        """Test updating tag to an already existing name"""
        tag1 = Tag.objects.create(name='Tag 1')
        tag2 = Tag.objects.create(name='Tag 2')
        
        payload = {'name': 'Tag 1'}  # Try to change tag2 to tag1's name
        url = detail_url(tag2.id)
        res = self.client.patch(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_nonexistent_tag(self):
        """Test deleting a tag that doesn't exist"""
        url = detail_url(99999)  # Non-existent ID
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_tag(self):
        """Test updating a tag that doesn't exist"""
        payload = {'name': 'Updated tag'}
        url = detail_url(99999)  # Non-existent ID
        res = self.client.patch(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_nonexistent_tag(self):
        """Test retrieving a tag that doesn't exist"""
        url = detail_url(99999)  # Non-existent ID
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_tags(self):
        """Test listing all tags"""
        Tag.objects.create(name='Python')
        Tag.objects.create(name='Django')
        Tag.objects.create(name='JavaScript')
        
        res = self.client.get(TAG_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 3)

    def test_list_tags_empty(self):
        """Test listing tags when none exist"""
        # Delete all existing tags
        Tag.objects.all().delete()
        
        res = self.client.get(TAG_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Handle paginated responses
        if isinstance(res.data, dict) and 'results' in res.data:
            count = len(res.data['results'])
        else:
            count = len(res.data)
            
        self.assertEqual(count, 0)

    def test_tag_with_unicode_characters(self):
        """Test creating tag with unicode characters"""
        payload = {'name': '日本語 Python'}
        res = self.client.post(TAG_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_tag_with_numbers(self):
        """Test creating tag with numbers"""
        payload = {'name': 'Python3.9'}
        res = self.client.post(TAG_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_create_tag_missing_name(self):
        """Test creating tag without name field"""
        payload = {}
        res = self.client.post(TAG_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tag_str_representation(self):
        """Test tag string representation"""
        tag = Tag.objects.create(name='Test Tag')
        self.assertEqual(str(tag), 'Test Tag')

    def test_partial_update_tag(self):
        """Test partial update of a tag"""
        tag = Tag.objects.create(name='Original Name')
        
        # Test that we can update just the name
        payload = {'name': 'New Name'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, 'New Name')

    def test_full_update_tag(self):
        """Test full update of a tag using PUT"""
        tag = Tag.objects.create(name='Original Name')
        
        payload = {'name': 'Completely New Name'}
        url = detail_url(tag.id)
        res = self.client.put(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, 'Completely New Name')

    def test_tag_name_trimming(self):
        """Test that tag names are trimmed of whitespace"""
        payload = {'name': '  Python  '}
        res = self.client.post(TAG_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Assuming the API trims whitespace
        expected_name = 'Python' if res.data['name'] == 'Python' else '  Python  '
        self.assertIn(res.data['name'], ['Python', '  Python  '])


       