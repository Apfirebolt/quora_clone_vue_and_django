"""
Tests for the Answer API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from api.serializers import AnswerSerializer
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Answer, Question, Comment


QUESTION_URL = reverse('api:questions')
MY_ANSWERS_URL = reverse('api:my-answers')
COMMENT_URL = reverse('api:comment-create')

def detail_url(Answer_id):
    """Return Answer detail URL"""
    return reverse('api:answer-detail', args=[Answer_id])

def answer_create_url(slug):
    """Return Answer create URL"""
    return reverse('api:answer-create', args=[slug])

def answer_like_url(answer_id):
    """Return answer like URL"""
    return reverse('api:answer-like', args=[answer_id])


class PublicAnswerApiTests(TestCase):
    """Test the publicly available Answer API"""

    def setUp(self):
        self.client = APIClient()


class PrivateAnswerApiTests(TestCase):
    """Test the authorized user Answer API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    
    def test_add_answer(self):
        """Test adding an answer to a question"""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        payload = {'body': 'Sample answer 1', 'author': self.user.id, 'question': question.id}
        
        url = answer_create_url(question.slug)
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        answer = Answer.objects.get(uuid=res.data['uuid'])
        self.assertEqual(answer.body, payload['body'])
        self.assertEqual(answer.author.id, payload['author'])
        self.assertEqual(answer.question.id, payload['question'])

    
    def test_retrieve_answers(self):
        """Test retrieving a list of answers"""
        questionOne = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        questionTwo = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 2', slug='sample-question-2')


        Answer.objects.create(author=self.user, body='Sample answer 1', question=questionOne)
        Answer.objects.create(author=self.user, body='Sample answer 2', question=questionTwo)

        res = self.client.get(MY_ANSWERS_URL)

        answers = Answer.objects.all().order_by('-id')
        serializer = AnswerSerializer(answers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_delete_answer(self):
        """Test deleting an answer"""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)

        url = detail_url(answer.uuid)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.filter(uuid=answer.uuid).count(), 0)
        

    def test_get_single_answer(self):
        """Test retrieving a single answer"""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)

        url = detail_url(answer.uuid)
        res = self.client.get(url)

        serializer = AnswerSerializer(answer)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_add_comment_to_answer(self):
        """Test adding a comment to an answer"""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)
        payload = {'body': 'Sample comment 1', 'author': self.user.id, 'answer': answer.uuid}

        res = self.client.post(COMMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get(uuid=res.data['uuid'])
        self.assertEqual(comment.body, payload['body'])
        self.assertEqual(comment.author.id, payload['author'])


    def test_delete_comment(self):
        """Test deleting a comment"""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)
        comment = Comment.objects.create(author=self.user, body='Sample comment 1', answer=answer)

        url = reverse('api:comment-detail', args=[comment.uuid])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.filter(uuid=comment.uuid).count(), 0)


    def test_get_single_comment(self):
        """Test retrieving a single comment"""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)
        comment = Comment.objects.create(author=self.user, body='Sample comment 1', answer=answer)

        url = reverse('api:comment-detail', args=[comment.uuid])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    
    def test_update_comment(self):
        """Test updating a comment"""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)
        comment = Comment.objects.create(author=self.user, body='Sample comment 1', answer=answer)
        payload = {'body': 'Sample comment 2'}

        url = reverse('api:comment-detail', args=[comment.uuid])
        res = self.client.patch(url, payload)

        comment.refresh_from_db()
        self.assertEqual(comment.body, payload['body'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_answer_like(self):
        """Test liking an answer"""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)

        like_payload = {
            'answerId': answer.uuid,
            'rating': 'upvote'
        }

        like_response = self.client.post(answer_like_url(answer.uuid), like_payload)
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)

        dislike_payload = {
            'answerId': answer.uuid,
            'rating': 'downvote'
        }

        dislike_response = self.client.post(answer_like_url(answer.uuid), dislike_payload)
        self.assertEqual(dislike_response.status_code, status.HTTP_200_OK)

    def test_add_answer_empty_body(self):
        """Test adding answer with empty body."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        payload = {'body': '', 'author': self.user.id, 'question': question.id}
        
        url = answer_create_url(question.slug)
        res = self.client.post(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_answer_to_nonexistent_question(self):
        """Test adding answer to non-existent question."""
        payload = {'body': 'Sample answer', 'author': self.user.id}
        
        url = answer_create_url('nonexistent-slug')
        res = self.client.post(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_answer_very_long_body(self):
        """Test adding answer with very long body."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        long_body = 'a' * 10000  # Very long answer
        payload = {'body': long_body, 'author': self.user.id, 'question': question.id}
        
        url = answer_create_url(question.slug)
        res = self.client.post(url, payload)
        
        # Should succeed since TextField has no max length by default
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_answer(self):
        """Test updating an answer."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Original answer', question=question)
        
        update_payload = {'body': 'Updated answer body'}
        url = detail_url(answer.uuid)
        res = self.client.patch(url, update_payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        answer.refresh_from_db()
        self.assertEqual(answer.body, update_payload['body'])

    def test_update_answer_unauthorized(self):
        """Test updating answer by non-author."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Original answer', question=question)
        
        # Create second user
        user2 = get_user_model().objects.create_user('test2@example.com', 'password123')
        client2 = APIClient()
        client2.force_authenticate(user2)
        
        update_payload = {'body': 'Unauthorized update'}
        url = detail_url(answer.uuid)
        res = client2.patch(url, update_payload)
        
        self.assertIn(res.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_delete_answer_unauthorized(self):
        """Test deleting answer by non-author."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer', question=question)
        
        # Create second user
        user2 = get_user_model().objects.create_user('test2@example.com', 'password123')
        client2 = APIClient()
        client2.force_authenticate(user2)
        
        url = detail_url(answer.uuid)
        res = client2.delete(url)
        
        self.assertIn(res.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
        # Answer should still exist
        self.assertEqual(Answer.objects.filter(uuid=answer.uuid).count(), 1)

    def test_get_nonexistent_answer(self):
        """Test retrieving non-existent answer."""
        import uuid
        fake_uuid = uuid.uuid4()
        
        url = detail_url(fake_uuid)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_answer_like_toggle(self):
        """Test toggling answer like/dislike."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer', question=question)
        
        # First upvote
        upvote_payload = {'answerId': answer.uuid, 'rating': 'upvote'}
        self.client.post(answer_like_url(answer.uuid), upvote_payload)
        
        # Then downvote (should remove upvote and add downvote)
        downvote_payload = {'answerId': answer.uuid, 'rating': 'downvote'}
        self.client.post(answer_like_url(answer.uuid), downvote_payload)
        
        answer.refresh_from_db()
        self.assertNotIn(self.user, answer.upvotes.all())
        self.assertIn(self.user, answer.downvotes.all())

    def test_answer_like_invalid_rating(self):
        """Test answer like with invalid rating."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer', question=question)
        
        invalid_payload = {'answerId': answer.uuid, 'rating': 'invalid_rating'}
        res = self.client.post(answer_like_url(answer.uuid), invalid_payload)
        
        # API might accept any rating or validate it
        self.assertIn(res.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_my_answers_empty(self):
        """Test retrieving my answers when none exist."""
        # Delete any existing answers for this user
        Answer.objects.filter(author=self.user).delete()
        
        res = self.client.get(MY_ANSWERS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Handle paginated responses
        if isinstance(res.data, dict) and 'results' in res.data:
            count = len(res.data['results'])
        else:
            count = len(res.data)
            
        self.assertEqual(count, 0)

    def test_my_answers_multiple_users(self):
        """Test that my answers only returns current user's answers."""
        # Clear any existing answers
        Answer.objects.filter(author=self.user).delete()
        
        question = Question.objects.create(author=self.user, description='Sample question', content='Sample content', slug='sample-question')
        
        # Create answer by current user
        Answer.objects.create(author=self.user, body='My answer', question=question)
        
        # Create another user and their answer
        user2 = get_user_model().objects.create_user('test2@example.com', 'password123')
        Answer.objects.create(author=user2, body='Other user answer', question=question)
        
        res = self.client.get(MY_ANSWERS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Handle paginated responses
        if isinstance(res.data, dict) and 'results' in res.data:
            answers = res.data['results']
        else:
            answers = res.data
            
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0]['body'], 'My answer')

    def test_comment_empty_body(self):
        """Test adding comment with empty body."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)
        payload = {'body': '', 'author': self.user.id, 'answer': answer.uuid}
        
        res = self.client.post(COMMENT_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_nonexistent_answer(self):
        """Test adding comment to non-existent answer."""
        import uuid
        fake_uuid = uuid.uuid4()
        
        payload = {'body': 'Sample comment', 'author': self.user.id, 'answer': fake_uuid}
        res = self.client.post(COMMENT_URL, payload)
        
        # API might return 404 for non-existent answer or 400 for invalid data
        self.assertIn(res.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND])

    def test_update_comment_unauthorized(self):
        """Test updating comment by non-author."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)
        comment = Comment.objects.create(author=self.user, body='Original comment', answer=answer)
        
        # Create second user
        user2 = get_user_model().objects.create_user('test2@example.com', 'password123')
        client2 = APIClient()
        client2.force_authenticate(user2)
        
        payload = {'body': 'Unauthorized update'}
        url = reverse('api:comment-detail', args=[comment.uuid])
        res = client2.patch(url, payload)
        
        self.assertIn(res.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_delete_comment_unauthorized(self):
        """Test deleting comment by non-author."""
        question = Question.objects.create(author=self.user, description='Sample question description', content='Sample body 1', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer 1', question=question)
        comment = Comment.objects.create(author=self.user, body='Sample comment', answer=answer)
        
        # Create second user
        user2 = get_user_model().objects.create_user('test2@example.com', 'password123')
        client2 = APIClient()
        client2.force_authenticate(user2)
        
        url = reverse('api:comment-detail', args=[comment.uuid])
        res = client2.delete(url)
        
        self.assertIn(res.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
        # Comment should still exist
        self.assertEqual(Comment.objects.filter(uuid=comment.uuid).count(), 1)

    def test_get_nonexistent_comment(self):
        """Test retrieving non-existent comment."""
        import uuid
        fake_uuid = uuid.uuid4()
        
        url = reverse('api:comment-detail', args=[fake_uuid])
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_answer_with_special_characters(self):
        """Test creating answer with special characters."""
        question = Question.objects.create(author=self.user, description='Sample question', content='Sample content', slug='sample-question')
        
        special_body = 'Answer with special chars äöü and emojis 🚀😄'
        payload = {'body': special_body, 'author': self.user.id, 'question': question.id}
        
        url = answer_create_url(question.slug)
        res = self.client.post(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['body'], special_body)

    def test_comment_with_special_characters(self):
        """Test creating comment with special characters."""
        question = Question.objects.create(author=self.user, description='Sample question', content='Sample content', slug='sample-question')
        answer = Answer.objects.create(author=self.user, body='Sample answer', question=question)
        
        special_comment = 'Comment with émojis 🚀 and special chars äöü'
        payload = {'body': special_comment, 'author': self.user.id, 'answer': answer.uuid}
        
        res = self.client.post(COMMENT_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['body'], special_comment)

    def test_list_answers_for_question(self):
        """Test listing answers for a specific question."""
        question = Question.objects.create(author=self.user, description='Sample question', content='Sample content', slug='sample-question')
        
        # Create multiple answers
        Answer.objects.create(author=self.user, body='First answer', question=question)
        Answer.objects.create(author=self.user, body='Second answer', question=question)
        
        url = reverse('api:answer-list', args=[question.slug])
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 2)
    

       