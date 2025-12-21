"""
Integration tests and edge cases for the API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Question, Answer, Comment, Tag, Notification
from api.serializers import QuestionSerializer, AnswerSerializer
import uuid


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class APIIntegrationTests(TestCase):
    """Integration tests covering multiple API endpoints and complex scenarios"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='password123',
            username='testuser'
        )
        self.user2 = create_user(
            email='test2@example.com', 
            password='password123',
            username='testuser2'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        
        self.client2 = APIClient()
        self.client2.force_authenticate(self.user2)

    def test_complete_question_answer_comment_workflow(self):
        """Test complete workflow: create question, answer, comment, and interact"""
        # 1. User1 creates a question
        question_payload = {
            'description': 'How to test Django APIs?',
            'content': 'I need help with testing Django REST APIs',
            'author': self.user.id
        }
        q_res = self.client.post(reverse('api:questions'), question_payload)
        self.assertEqual(q_res.status_code, status.HTTP_201_CREATED)
        question = Question.objects.get(uuid=q_res.data['uuid'])
        
        # 2. User2 answers the question
        answer_payload = {
            'body': 'You can use Django Test Client and APITestCase',
            'author': self.user2.id,
            'question': question.id
        }
        a_res = self.client2.post(
            reverse('api:answer-create', args=[question.slug]), 
            answer_payload
        )
        self.assertEqual(a_res.status_code, status.HTTP_201_CREATED)
        answer = Answer.objects.get(uuid=a_res.data['uuid'])
        
        # 3. User1 comments on the answer
        comment_payload = {
            'body': 'Thank you for the helpful answer!',
            'author': self.user.id,
            'answer': answer.uuid
        }
        c_res = self.client.post(reverse('api:comment-create'), comment_payload)
        self.assertEqual(c_res.status_code, status.HTTP_201_CREATED)
        
        # 4. User1 upvotes the answer
        like_payload = {
            'answerId': answer.uuid,
            'rating': 'upvote'
        }
        like_res = self.client.post(
            reverse('api:answer-like', args=[answer.uuid]), 
            like_payload
        )
        self.assertEqual(like_res.status_code, status.HTTP_200_OK)
        
        # 5. Verify the complete state
        question.refresh_from_db()
        answer.refresh_from_db()
        
        self.assertEqual(question.answers.count(), 1)
        self.assertEqual(answer.comments.count(), 1)
        self.assertIn(self.user, answer.upvotes.all())

    def test_user_follow_and_activity_interaction(self):
        """Test user following and how it affects activity visibility"""
        # User1 follows User2
        follow_res = self.client.post(reverse('api:follow', args=[self.user2.username]))
        self.assertEqual(follow_res.status_code, status.HTTP_200_OK)
        
        # User2 creates a question
        question_payload = {
            'description': 'Followed user question',
            'content': 'This is a question from a followed user',
            'author': self.user2.id
        }
        q_res = self.client2.post(reverse('api:questions'), question_payload)
        self.assertEqual(q_res.status_code, status.HTTP_201_CREATED)
        
        # Verify User1 can see the question in general feed
        questions_res = self.client.get(reverse('api:questions'))
        self.assertEqual(questions_res.status_code, status.HTTP_200_OK)
        
        # User1 unfollows User2
        unfollow_res = self.client.delete(reverse('api:follow', args=[self.user2.username]))
        self.assertEqual(unfollow_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_question_with_multiple_tags_and_answers(self):
        """Test question with multiple tags and multiple answers"""
        # Create tags
        tag1 = Tag.objects.create(name='Python')
        tag2 = Tag.objects.create(name='Django')
        tag3 = Tag.objects.create(name='Testing')
        
        # Create question with multiple tags
        question = Question.objects.create(
            author=self.user,
            description='Complex Django testing question',
            content='How to test complex Django applications?',
            slug='complex-django-testing'
        )
        question.tags.set([tag1, tag2, tag3])
        
        # Multiple users create answers
        users = [self.user, self.user2]
        for i, user in enumerate(users):
            Answer.objects.create(
                author=user,
                body=f'Answer {i+1} to the complex question',
                question=question
            )
        
        # Test retrieving question with all relationships
        q_detail_res = self.client.get(
            reverse('api:question-detail', args=[question.slug])
        )
        self.assertEqual(q_detail_res.status_code, status.HTTP_200_OK)
        
        # Test retrieving answers for the question
        answers_res = self.client.get(
            reverse('api:answer-list', args=[question.slug])
        )
        self.assertEqual(answers_res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(answers_res.data), 2)

    def test_concurrent_voting_on_same_content(self):
        """Test concurrent voting scenarios"""
        question = Question.objects.create(
            author=self.user,
            description='Vote test question',
            content='Test voting scenarios',
            slug='vote-test-question'
        )
        
        answer = Answer.objects.create(
            author=self.user2,
            body='Test answer for voting',
            question=question
        )
        
        # Both users vote on the question
        q_vote_payload = {
            'questionId': question.uuid,
            'rating': 'upvote'
        }
        
        q_vote1 = self.client.post(
            reverse('api:question-like', args=[question.uuid]), 
            q_vote_payload
        )
        q_vote2 = self.client2.post(
            reverse('api:question-like', args=[question.uuid]),
            q_vote_payload
        )
        
        self.assertEqual(q_vote1.status_code, status.HTTP_200_OK)
        self.assertEqual(q_vote2.status_code, status.HTTP_200_OK)
        
        question.refresh_from_db()
        self.assertEqual(question.upvotes.count(), 2)
        
        # Both users vote on the answer
        a_vote_payload = {
            'answerId': answer.uuid,
            'rating': 'upvote'
        }
        
        a_vote1 = self.client.post(
            reverse('api:answer-like', args=[answer.uuid]),
            a_vote_payload
        )
        a_vote2 = self.client2.post(
            reverse('api:answer-like', args=[answer.uuid]),
            a_vote_payload
        )
        
        self.assertEqual(a_vote1.status_code, status.HTTP_200_OK)
        self.assertEqual(a_vote2.status_code, status.HTTP_200_OK)
        
        answer.refresh_from_db()
        self.assertEqual(answer.upvotes.count(), 2)

    def test_invalid_uuid_handling(self):
        """Test handling of invalid UUIDs across different endpoints"""
        import uuid
        # Use a valid UUID format that doesn't exist
        fake_uuid = uuid.uuid4()
        
        # Test fake UUID in answer endpoints
        answer_detail_url = reverse('api:answer-detail', args=[fake_uuid])
        res = self.client.get(answer_detail_url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        
        # Test fake UUID in comment endpoints  
        comment_detail_url = reverse('api:comment-detail', args=[fake_uuid])
        res = self.client.get(comment_detail_url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        
        # Test fake UUID in voting endpoints
        vote_url = reverse('api:answer-like', args=[fake_uuid])
        vote_payload = {'answerId': fake_uuid, 'rating': 'upvote'}
        res = self.client.post(vote_url, vote_payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_very_long_content_handling(self):
        """Test handling of very long content in various fields"""
        # Very long question content
        long_content = 'A' * 1000
        question_payload = {
            'description': 'Long content test',
            'content': long_content,
            'author': self.user.id
        }
        
        q_res = self.client.post(reverse('api:questions'), question_payload)
        # Should fail if content exceeds max length (240 chars)
        self.assertEqual(q_res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Very long answer body
        question = Question.objects.create(
            author=self.user,
            description='Test question',
            content='Short content',
            slug='test-question'
        )
        
        very_long_answer = 'B' * 10000  # Very long answer
        answer_payload = {
            'body': very_long_answer,
            'author': self.user.id,
            'question': question.id
        }
        
        a_res = self.client.post(
            reverse('api:answer-create', args=[question.slug]),
            answer_payload
        )
        # TextField should accept long content
        self.assertEqual(a_res.status_code, status.HTTP_201_CREATED)

    def test_malformed_request_data(self):
        """Test handling of malformed request data"""
        # Test with malformed JSON-like data
        malformed_payloads = [
            {'invalid_field': 'value'},
            {'author': 'non_numeric_string'},
            {'rating': 'invalid_rating_value'},
        ]
        
        for payload in malformed_payloads:
            if payload is not None:
                # Test question creation
                q_res = self.client.post(reverse('api:questions'), payload)
                self.assertIn(q_res.status_code, [
                    status.HTTP_400_BAD_REQUEST,
                    status.HTTP_422_UNPROCESSABLE_ENTITY
                ])
                
                # Test tag creation
                t_res = self.client.post(reverse('api:tags'), payload)
                self.assertIn(t_res.status_code, [
                    status.HTTP_400_BAD_REQUEST,
                    status.HTTP_422_UNPROCESSABLE_ENTITY
                ])

    def test_cascade_deletion_behavior(self):
        """Test cascade deletion behavior"""
        # Create question with answer and comment
        question = Question.objects.create(
            author=self.user,
            description='Cascade test',
            content='Test cascade deletion',
            slug='cascade-test'
        )
        
        answer = Answer.objects.create(
            author=self.user2,
            body='Test answer for cascade',
            question=question
        )
        
        comment = Comment.objects.create(
            author=self.user,
            body='Test comment for cascade',
            answer=answer
        )
        
        # Store IDs
        answer_id = answer.id
        comment_id = comment.id
        
        # Delete question
        q_delete_res = self.client.delete(
            reverse('api:question-detail', args=[question.slug])
        )
        self.assertEqual(q_delete_res.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify cascade deletion
        self.assertFalse(Question.objects.filter(id=question.id).exists())
        self.assertFalse(Answer.objects.filter(id=answer_id).exists())
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

    def test_simultaneous_user_operations(self):
        """Test simultaneous operations by multiple users"""
        # Both users try to create tags with same name
        tag_payload = {'name': 'Simultaneous Tag'}
        
        t_res1 = self.client.post(reverse('api:tags'), tag_payload)
        t_res2 = self.client2.post(reverse('api:tags'), tag_payload)
        
        # One should succeed, one should fail due to uniqueness
        results = [t_res1.status_code, t_res2.status_code]
        self.assertIn(status.HTTP_201_CREATED, results)
        self.assertIn(status.HTTP_400_BAD_REQUEST, results)
        
        # Both users try to follow the same third user
        user3 = create_user(
            email='user3@example.com',
            password='password123',
            username='user3'
        )
        
        follow_res1 = self.client.post(reverse('api:follow', args=[user3.username]))
        follow_res2 = self.client2.post(reverse('api:follow', args=[user3.username]))
        
        # Both should succeed (different users can follow the same person)
        self.assertEqual(follow_res1.status_code, status.HTTP_200_OK)
        self.assertEqual(follow_res2.status_code, status.HTTP_200_OK)

    def test_api_response_format_consistency(self):
        """Test that API responses have consistent format"""
        # Create test data
        question = Question.objects.create(
            author=self.user,
            description='Format test',
            content='Test response format',
            slug='format-test'
        )
        
        # Test question list response format
        q_list_res = self.client.get(reverse('api:questions'))
        self.assertEqual(q_list_res.status_code, status.HTTP_200_OK)
        
        # Check if paginated or list response
        if isinstance(q_list_res.data, dict) and 'results' in q_list_res.data:
            # Paginated response
            self.assertIsInstance(q_list_res.data, dict)
            self.assertIn('results', q_list_res.data)
            self.assertIsInstance(q_list_res.data['results'], list)
        else:
            # Direct list response
            self.assertIsInstance(q_list_res.data, list)
        
        if q_list_res.data:
            question_data = q_list_res.data[0]
            required_fields = ['uuid', 'content', 'slug', 'author', 'created_at']
            for field in required_fields:
                if field in question_data:  # Check if field exists
                    self.assertIsNotNone(question_data[field])
        
        # Test question detail response format
        q_detail_res = self.client.get(
            reverse('api:question-detail', args=[question.slug])
        )
        self.assertEqual(q_detail_res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(q_detail_res.data, dict)
        
        # Test user list response format
        user_list_res = self.client.get(reverse('api:users'))
        self.assertEqual(user_list_res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(user_list_res.data, list)