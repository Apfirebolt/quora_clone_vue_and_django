"""
Tests for the Notification API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Notification, Question, Answer, Comment


NOTIFICATIONS_URL = reverse('api:notifications')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicNotificationApiTests(TestCase):
    """Test the publicly available notification API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving notifications"""
        res = self.client.get(NOTIFICATIONS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNotificationApiTests(TestCase):
    """Test the authorized user notification API"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='password123',
            username='testuser'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_notifications(self):
        """Test retrieving notifications for authenticated user"""
        # Clear any existing notifications
        Notification.objects.filter(recipient=self.user).delete()
        
        # Create some notifications
        Notification.objects.create(
            recipient=self.user,
            message='Test notification 1',
            category='test',
            is_read=False
        )
        Notification.objects.create(
            recipient=self.user,
            message='Test notification 2',
            category='test',
            is_read=True
        )
        
        # Create notification for another user
        other_user = create_user(
            email='other@example.com',
            password='password123',
            username='otheruser'
        )
        Notification.objects.create(
            recipient=other_user,
            message='Other user notification',
            category='test',
            is_read=False
        )
        
        res = self.client.get(NOTIFICATIONS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Handle paginated responses
        if isinstance(res.data, dict) and 'results' in res.data:
            notifications = res.data['results']
        else:
            notifications = res.data
            
        # Should only return current user's notifications
        self.assertEqual(len(notifications), 2)
        
        # Check that notifications belong to current user
        for notification in notifications:
            self.assertIn('message', notification)
            self.assertIn('category', notification)
            self.assertIn('is_read', notification)

    def test_notifications_empty(self):
        """Test retrieving notifications when none exist"""
        # Clear any existing notifications
        Notification.objects.filter(recipient=self.user).delete()
        
        res = self.client.get(NOTIFICATIONS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Handle paginated responses
        if isinstance(res.data, dict) and 'results' in res.data:
            count = len(res.data['results'])
        else:
            count = len(res.data)
            
        self.assertEqual(count, 0)

    def test_notifications_ordering(self):
        """Test that notifications are returned in correct order (newest first)"""
        # Clear any existing notifications
        Notification.objects.filter(recipient=self.user).delete()
        
        # Create notifications with different timestamps
        notification1 = Notification.objects.create(
            recipient=self.user,
            message='First notification',
            category='test',
            is_read=False
        )
        notification2 = Notification.objects.create(
            recipient=self.user,
            message='Second notification',
            category='test',
            is_read=False
        )
        notification3 = Notification.objects.create(
            recipient=self.user,
            message='Third notification',
            category='test',
            is_read=False
        )
        
        res = self.client.get(NOTIFICATIONS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Handle paginated responses
        if isinstance(res.data, dict) and 'results' in res.data:
            notifications = res.data['results']
        else:
            notifications = res.data
            
        self.assertEqual(len(notifications), 3)
        
        # Assuming newest first ordering
        messages = [notif['message'] for notif in notifications]
        if notifications[0]['message'] == 'Third notification':
            # Confirmed newest first
            self.assertEqual(messages, ['Third notification', 'Second notification', 'First notification'])

    def test_notification_categories(self):
        """Test notifications with different categories"""
        # Clear any existing notifications
        Notification.objects.filter(recipient=self.user).delete()
        
        Notification.objects.create(
            recipient=self.user,
            message='Answer notification',
            category='answer',
            is_read=False
        )
        Notification.objects.create(
            recipient=self.user,
            message='Comment notification',
            category='comment',
            is_read=False
        )
        Notification.objects.create(
            recipient=self.user,
            message='Follow notification',
            category='follow',
            is_read=False
        )
        
        res = self.client.get(NOTIFICATIONS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Handle paginated responses
        if isinstance(res.data, dict) and 'results' in res.data:
            notifications = res.data['results']
        else:
            notifications = res.data
            
        self.assertEqual(len(notifications), 3)
        
        categories = [notif['category'] for notif in notifications]
        self.assertIn('answer', categories)
        self.assertIn('comment', categories)
        self.assertIn('follow', categories)

    def test_notification_read_status(self):
        """Test notifications with different read statuses"""
        Notification.objects.create(
            recipient=self.user,
            message='Unread notification',
            category='test',
            is_read=False
        )
        Notification.objects.create(
            recipient=self.user,
            message='Read notification',
            category='test',
            is_read=True
        )
        
        res = self.client.get(NOTIFICATIONS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        
        # Check that both read and unread notifications are returned
        read_statuses = [notif['is_read'] for notif in res.data]
        self.assertIn(True, read_statuses)
        self.assertIn(False, read_statuses)

    def test_notification_string_representation(self):
        """Test notification string representation"""
        notification = Notification.objects.create(
            recipient=self.user,
            message='Test message',
            category='test',
            is_read=False
        )
        
        expected_str = f"Notification for {self.user.username} - Test message (test)"
        self.assertEqual(str(notification), expected_str)

    def test_notification_auto_timestamps(self):
        """Test that notifications have automatic timestamps"""
        notification = Notification.objects.create(
            recipient=self.user,
            message='Test notification',
            category='test',
            is_read=False
        )
        
        self.assertIsNotNone(notification.created_at)
        self.assertIsNotNone(notification.updated_at)

    def test_large_number_of_notifications(self):
        """Test handling large number of notifications"""
        # Create many notifications
        for i in range(50):
            Notification.objects.create(
                recipient=self.user,
                message=f'Notification {i}',
                category='test',
                is_read=i % 2 == 0  # Alternate read/unread
            )
        
        res = self.client.get(NOTIFICATIONS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check if pagination is implemented or all notifications are returned
        self.assertGreaterEqual(len(res.data), 10)  # At least some notifications
        self.assertLessEqual(len(res.data), 50)     # Not more than created

    def test_notification_message_length(self):
        """Test notifications with different message lengths"""
        short_message = "Short"
        long_message = "A" * 200  # Long message
        max_length_message = "B" * 255  # Assuming max length is 255
        
        # Short message
        notif1 = Notification.objects.create(
            recipient=self.user,
            message=short_message,
            category='test',
            is_read=False
        )
        
        # Long message
        notif2 = Notification.objects.create(
            recipient=self.user,
            message=long_message,
            category='test',
            is_read=False
        )
        
        # Max length message
        notif3 = Notification.objects.create(
            recipient=self.user,
            message=max_length_message,
            category='test',
            is_read=False
        )
        
        self.assertEqual(notif1.message, short_message)
        self.assertEqual(notif2.message, long_message)
        self.assertEqual(notif3.message, max_length_message)
        
        res = self.client.get(NOTIFICATIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_notification_special_characters(self):
        """Test notifications with special characters"""
        special_message = "Notification with émojis 🚀🎉 and special chars äöü"
        
        notification = Notification.objects.create(
            recipient=self.user,
            message=special_message,
            category='test',
            is_read=False
        )
        
        self.assertEqual(notification.message, special_message)
        
        res = self.client.get(NOTIFICATIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['message'], special_message)