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
    

       