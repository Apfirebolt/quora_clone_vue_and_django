"""
Tests for the Question API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from api.serializers import QuestionSerializer
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Question


QUESTION_URL = reverse('api:questions')
MY_QUESTIONS_URL = reverse('api:my-questions')


def detail_url(question_id):
    """Return question detail URL"""
    return reverse('api:question-detail', args=[question_id])


class PublicQuestionApiTests(TestCase):
    """Test the publicly available question API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving questions"""
        res = self.client.get(QUESTION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateQuestionApiTests(TestCase):
    """Test the authorized user question API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)


    def test_retrieve_questions(self):
        """Test retrieving a list of questions"""
        Question.objects.create(author=self.user, slug='Sample question 1', content='Sample body 1')
        Question.objects.create(author=self.user, slug='Sample question 2', content='Sample body 2')

        res = self.client.get(QUESTION_URL)

        questions = Question.objects.all().order_by('-id')
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_question(self):
        """Test creating question"""
        payload = {'slug': 'sample-question-1', 'content': 'Sample body 1', 'author': self.user.id}
        res = self.client.post(QUESTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['content'], payload['content'])

    def test_get_question_detail(self):
        """Test viewing a question detail"""

        payload = {'description': 'sample-question-1', 'content': 'Sample body 1', 'author': self.user.id}
        res = self.client.post(QUESTION_URL, payload)

        question = Question.objects.get(uuid=res.data['uuid'])

        get_response = self.client.get(detail_url(question.slug))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_update_question(self):
        """Test updating a question"""
        payload = {'description': 'sample-question-1', 'content': 'Sample body 1', 'author': self.user.id}
        res = self.client.post(QUESTION_URL, payload)

        question = Question.objects.get(uuid=res.data['uuid'])

        update_payload = {'description': 'sample-question-1', 'content': 'Sample body 1 updated', 'author': self.user.id}
        update_response = self.client.put(detail_url(question.slug), update_payload)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)


    def test_delete_question(self):
        """Test deleting a question"""

        payload = {'description': 'sample-question-1', 'content': 'Sample body 1', 'author': self.user.id}
        res = self.client.post(QUESTION_URL, payload)

        question = Question.objects.get(uuid=res.data['uuid'])

        delete_response = self.client.delete(detail_url(question.slug))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        get_response = self.client.get(detail_url(question.slug))
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_my_questions(self):
        """Test retrieving questions for user"""
        Question.objects.create(author=self.user, slug='Sample question 1', content='Sample body 1')
        Question.objects.create(author=self.user, slug='Sample question 2', content='Sample body 2')

        res = self.client.get(MY_QUESTIONS_URL)

        questions = Question.objects.filter(author=self.user)
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

       