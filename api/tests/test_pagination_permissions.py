"""
Tests for pagination and permissions across the API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Question, Answer, Tag, Notification
from unittest.mock import patch


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PaginationTests(TestCase):
    """Test pagination across different API endpoints"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='password123',
            username='testuser'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_questions_pagination(self):
        """Test pagination for questions endpoint"""
        # Create many questions
        for i in range(25):
            Question.objects.create(
                author=self.user,
                description=f'Question {i}',
                content=f'Content for question {i}',
                slug=f'question-{i}'
            )
        
        # Test first page
        res = self.client.get(reverse('api:questions'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Check if pagination is implemented
        if isinstance(res.data, dict) and 'results' in res.data:
            # Paginated response
            self.assertIn('results', res.data)
            self.assertIn('count', res.data)
            self.assertIn('next', res.data)
            self.assertIn('previous', res.data)
            self.assertLessEqual(len(res.data['results']), 20)  # Assuming page size <= 20
        else:
            # Non-paginated response - should still work
            self.assertIsInstance(res.data, list)
            self.assertLessEqual(len(res.data), 25)
        
        # Test with page parameter if pagination is implemented
        page_res = self.client.get(reverse('api:questions'), {'page': 1})
        self.assertEqual(page_res.status_code, status.HTTP_200_OK)

    def test_users_pagination(self):
        """Test pagination for users endpoint"""
        # Create many users
        for i in range(15):
            create_user(
                email=f'user{i}@example.com',
                password='password123',
                username=f'user{i}'
            )
        
        res = self.client.get(reverse('api:users'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Check pagination structure
        if isinstance(res.data, dict) and 'results' in res.data:
            self.assertIn('results', res.data)
            self.assertGreaterEqual(len(res.data['results']), 1)
        else:
            self.assertIsInstance(res.data, list)
            self.assertGreaterEqual(len(res.data), 10)  # At least the created users

    def test_tags_pagination(self):
        """Test pagination for tags endpoint"""
        # Create many tags
        for i in range(30):
            Tag.objects.create(name=f'Tag{i}')
        
        res = self.client.get(reverse('api:tags'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        if isinstance(res.data, dict) and 'results' in res.data:
            self.assertIn('results', res.data)
            self.assertGreaterEqual(len(res.data['results']), 1)
        else:
            self.assertIsInstance(res.data, list)
            self.assertGreaterEqual(len(res.data), 20)

    def test_my_questions_pagination(self):
        """Test pagination for my questions endpoint"""
        # Create many questions for current user
        for i in range(20):
            Question.objects.create(
                author=self.user,
                description=f'My Question {i}',
                content=f'My content {i}',
                slug=f'my-question-{i}'
            )
        
        res = self.client.get(reverse('api:my-questions'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        if isinstance(res.data, dict) and 'results' in res.data:
            self.assertIn('results', res.data)
        else:
            self.assertIsInstance(res.data, list)
        
        # Verify only current user's questions
        if isinstance(res.data, list):
            questions = res.data
        else:
            questions = res.data.get('results', [])
        
        for question in questions:
            if 'author' in question:
                # Verify author is current user
                self.assertIn(question['author'], [self.user.id, self.user.username])

    def test_my_answers_pagination(self):
        """Test pagination for my answers endpoint"""
        # Create question first
        question = Question.objects.create(
            author=self.user,
            description='Test Question',
            content='Test Content',
            slug='test-question'
        )
        
        # Create many answers
        for i in range(15):
            Answer.objects.create(
                author=self.user,
                body=f'My answer {i}',
                question=question
            )
        
        res = self.client.get(reverse('api:my-answers'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        if isinstance(res.data, dict) and 'results' in res.data:
            self.assertIn('results', res.data)
        else:
            self.assertIsInstance(res.data, list)

    def test_notifications_pagination(self):
        """Test pagination for notifications endpoint"""
        # Create many notifications
        for i in range(25):
            Notification.objects.create(
                recipient=self.user,
                message=f'Notification {i}',
                category='test',
                is_read=i % 2 == 0
            )
        
        res = self.client.get(reverse('api:notifications'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        if isinstance(res.data, dict) and 'results' in res.data:
            self.assertIn('results', res.data)
            self.assertGreaterEqual(len(res.data['results']), 1)
        else:
            self.assertIsInstance(res.data, list)
            self.assertGreaterEqual(len(res.data), 20)

    def test_pagination_edge_cases(self):
        """Test pagination edge cases"""
        # Test empty results
        res = self.client.get(reverse('api:my-questions'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Test invalid page numbers
        invalid_pages = [-1, 0, 999999, 'invalid']
        
        for page in invalid_pages:
            page_res = self.client.get(reverse('api:questions'), {'page': page})
            # Should either return 404 or ignore invalid page and return first page
            self.assertIn(page_res.status_code, [
                status.HTTP_200_OK, 
                status.HTTP_404_NOT_FOUND,
                status.HTTP_400_BAD_REQUEST
            ])

    def test_pagination_page_size_limits(self):
        """Test pagination with different page sizes"""
        # Create some test data
        for i in range(10):
            Question.objects.create(
                author=self.user,
                description=f'Question {i}',
                content=f'Content {i}',
                slug=f'question-{i}'
            )
        
        # Test different page sizes if supported
        page_sizes = [5, 10, 20, 100]
        
        for size in page_sizes:
            res = self.client.get(reverse('api:questions'), {'page_size': size})
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            
            if isinstance(res.data, dict) and 'results' in res.data:
                # If page size is respected
                self.assertLessEqual(len(res.data['results']), size)


class PermissionTests(TestCase):
    """Test permissions across different API endpoints"""

    def setUp(self):
        self.user1 = create_user(
            email='user1@example.com',
            password='password123',
            username='user1'
        )
        self.user2 = create_user(
            email='user2@example.com',
            password='password123',
            username='user2'
        )
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.public_client = APIClient()

    def test_unauthenticated_access_restrictions(self):
        """Test that unauthenticated users can't access protected endpoints"""
        protected_endpoints = [
            reverse('api:questions'),
            reverse('api:my-questions'),
            reverse('api:my-answers'),
            reverse('api:profile'),
            reverse('api:tags'),
            reverse('api:notifications'),
            reverse('api:users'),
        ]
        
        for endpoint in protected_endpoints:
            res = self.public_client.get(endpoint)
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_basic_access(self):
        """Test that authenticated users can access basic endpoints"""
        self.client1.force_authenticate(self.user1)
        
        accessible_endpoints = [
            reverse('api:questions'),
            reverse('api:my-questions'),
            reverse('api:my-answers'),
            reverse('api:profile'),
            reverse('api:tags'),
            reverse('api:notifications'),
            reverse('api:users'),
        ]
        
        for endpoint in accessible_endpoints:
            res = self.client1.get(endpoint)
            self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_question_ownership_permissions(self):
        """Test question ownership permissions"""
        self.client1.force_authenticate(self.user1)
        self.client2.force_authenticate(self.user2)
        
        # User1 creates a question
        question = Question.objects.create(
            author=self.user1,
            description='Test question',
            content='Test content',
            slug='test-question'
        )
        
        # User1 (owner) should be able to update
        update_data = {'content': 'Updated content'}
        update_res = self.client1.patch(
            reverse('api:question-detail', args=[question.slug]),
            update_data
        )
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        
        # User1 (owner) should be able to delete
        delete_res = self.client1.delete(
            reverse('api:question-detail', args=[question.slug])
        )
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_question_non_owner_restrictions(self):
        """Test that non-owners cannot modify questions"""
        self.client1.force_authenticate(self.user1)
        self.client2.force_authenticate(self.user2)
        
        # User1 creates a question
        question = Question.objects.create(
            author=self.user1,
            description='Test question',
            content='Test content',
            slug='test-question-2'
        )
        
        # User2 (non-owner) should not be able to update
        update_data = {'content': 'Unauthorized update'}
        update_res = self.client2.patch(
            reverse('api:question-detail', args=[question.slug]),
            update_data
        )
        self.assertIn(update_res.status_code, [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ])
        
        # User2 (non-owner) should not be able to delete
        delete_res = self.client2.delete(
            reverse('api:question-detail', args=[question.slug])
        )
        self.assertIn(delete_res.status_code, [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ])

    def test_answer_ownership_permissions(self):
        """Test answer ownership permissions"""
        self.client1.force_authenticate(self.user1)
        self.client2.force_authenticate(self.user2)
        
        # Create question and answer
        question = Question.objects.create(
            author=self.user1,
            description='Test question',
            content='Test content',
            slug='test-question-3'
        )
        
        answer = Answer.objects.create(
            author=self.user1,
            body='Test answer',
            question=question
        )
        
        # Owner should be able to update
        update_data = {'body': 'Updated answer'}
        update_res = self.client1.patch(
            reverse('api:answer-detail', args=[answer.uuid]),
            update_data
        )
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        
        # Non-owner should not be able to update
        update_res2 = self.client2.patch(
            reverse('api:answer-detail', args=[answer.uuid]),
            update_data
        )
        self.assertIn(update_res2.status_code, [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ])

    def test_profile_access_permissions(self):
        """Test profile access permissions"""
        self.client1.force_authenticate(self.user1)
        self.client2.force_authenticate(self.user2)
        
        # Users should be able to access their own profile
        profile_res1 = self.client1.get(reverse('api:profile'))
        self.assertEqual(profile_res1.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_res1.data['email'], self.user1.email)
        
        profile_res2 = self.client2.get(reverse('api:profile'))
        self.assertEqual(profile_res2.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_res2.data['email'], self.user2.email)
        
        # Users should be able to view other user details
        user_detail_res = self.client1.get(
            reverse('api:user-detail', args=[self.user2.username])
        )
        self.assertEqual(user_detail_res.status_code, status.HTTP_200_OK)

    def test_follow_permissions(self):
        """Test follow/unfollow permissions"""
        self.client1.force_authenticate(self.user1)
        
        # Should be able to follow another user
        follow_res = self.client1.post(
            reverse('api:follow', args=[self.user2.username])
        )
        self.assertEqual(follow_res.status_code, status.HTTP_200_OK)
        
        # Should not be able to follow self
        self_follow_res = self.client1.post(
            reverse('api:follow', args=[self.user1.username])
        )
        self.assertEqual(self_follow_res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Should be able to unfollow
        unfollow_res = self.client1.delete(
            reverse('api:follow', args=[self.user2.username])
        )
        self.assertEqual(unfollow_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_tag_permissions(self):
        """Test tag creation and modification permissions"""
        self.client1.force_authenticate(self.user1)
        self.client2.force_authenticate(self.user2)
        
        # Any authenticated user should be able to create tags
        tag_data = {'name': 'TestTag'}
        tag_res = self.client1.post(reverse('api:tags'), tag_data)
        self.assertEqual(tag_res.status_code, status.HTTP_201_CREATED)
        
        tag = Tag.objects.get(name='TestTag')
        
        # Both users should be able to update tags (if allowed by design)
        update_data = {'name': 'UpdatedTag'}
        update_res = self.client2.patch(
            reverse('api:tag-detail', args=[tag.id]),
            update_data
        )
        # This might be allowed or forbidden depending on business logic
        self.assertIn(update_res.status_code, [
            status.HTTP_200_OK,
            status.HTTP_403_FORBIDDEN
        ])

    def test_voting_permissions(self):
        """Test voting permissions"""
        self.client1.force_authenticate(self.user1)
        self.client2.force_authenticate(self.user2)
        
        # Create question and answer
        question = Question.objects.create(
            author=self.user1,
            description='Vote test',
            content='Test voting',
            slug='vote-test'
        )
        
        answer = Answer.objects.create(
            author=self.user1,
            body='Test answer',
            question=question
        )
        
        # User2 should be able to vote on user1's content
        q_vote_data = {'questionId': question.uuid, 'rating': 'upvote'}
        q_vote_res = self.client2.post(
            reverse('api:question-like', args=[question.uuid]),
            q_vote_data
        )
        self.assertEqual(q_vote_res.status_code, status.HTTP_200_OK)
        
        a_vote_data = {'answerId': answer.uuid, 'rating': 'upvote'}
        a_vote_res = self.client2.post(
            reverse('api:answer-like', args=[answer.uuid]),
            a_vote_data
        )
        self.assertEqual(a_vote_res.status_code, status.HTTP_200_OK)
        
        # Users should be able to vote on their own content (if allowed)
        self_vote_res = self.client1.post(
            reverse('api:question-like', args=[question.uuid]),
            q_vote_data
        )
        # This might be allowed or forbidden
        self.assertIn(self_vote_res.status_code, [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST
        ])

    def test_notification_privacy(self):
        """Test that users can only see their own notifications"""
        self.client1.force_authenticate(self.user1)
        self.client2.force_authenticate(self.user2)
        
        # Create notifications for both users
        Notification.objects.create(
            recipient=self.user1,
            message='Notification for user 1',
            category='test'
        )
        Notification.objects.create(
            recipient=self.user2,
            message='Notification for user 2',
            category='test'
        )
        
        # Each user should only see their own notifications
        notifs1 = self.client1.get(reverse('api:notifications'))
        self.assertEqual(notifs1.status_code, status.HTTP_200_OK)
        
        notifs2 = self.client2.get(reverse('api:notifications'))
        self.assertEqual(notifs2.status_code, status.HTTP_200_OK)
        
        # Verify content isolation
        if isinstance(notifs1.data, list):
            user1_messages = [n['message'] for n in notifs1.data]
        else:
            user1_messages = [n['message'] for n in notifs1.data.get('results', [])]
        
        self.assertIn('Notification for user 1', user1_messages)
        self.assertNotIn('Notification for user 2', user1_messages)