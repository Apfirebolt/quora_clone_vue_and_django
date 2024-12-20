from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.text import slugify

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    AnswerSerializer,
    QuestionSerializer,
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
    CustomUserSerializer,
    ListUserSerializer,
    ProfileSerializer,
    UserDetailSerializer,
    CommentSerializer
)
from core.models import Answer, Question, Comment
from accounts.models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


class ListCustomUsersApiView(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)

        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserDetailApiView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "username"


class ListCreateQuestionsApiView(ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, slug=slugify(serializer.validated_data["content"])
        )


class RetrieveUpdateDestroyQuestionApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "slug"

    def delete(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        question.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        serializer = self.get_serializer(question, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MyQuestionsListAPIView(ListAPIView):

    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Question.objects.filter(author=user).order_by("-created_at")


class QuestionLikeAPIView(APIView):

    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def delete(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        user = request.user

        question.upvotes.remove(user)
        question.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(question, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, uuid):
        question = get_object_or_404(Question, uuid=uuid)
        rating = request.data.get("rating")
        user = request.user
        if rating == "upvote":
            question.upvotes.add(user)
        else:
            question.downvotes.add(user)

        question.save()
        serializer_context = {"request": request}
        serializer = self.serializer_class(question, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerCreateAPIView(CreateAPIView):
    """Allow users to answer a question instance if they haven't already."""

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=kwarg_slug)

        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question!")

        serializer.save(author=request_user, question=question)


class AnswerRUDAPIView(RetrieveUpdateDestroyAPIView):
    """Provide *RUD functionality for an answer instance to it's author."""

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "uuid"


class MyAnswersListAPIView(ListAPIView):
    """Provide the answers queryset of the request.user."""

    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Answer.objects.filter(author=user).order_by("-created_at")
    

class AnswerListAPIView(ListAPIView):
    """Provide the answers queryset of a specific question instance."""

    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answer.objects.filter(question__slug=kwarg_slug).order_by("-created_at")


class AnswerLikeAPIView(APIView):
    """Allow users to add/remove a like to/from an answer instance."""

    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def delete(self, request, uuid):
        """Remove request.user from the voters queryset of an answer instance."""
        answer = get_object_or_404(Answer, uuid=uuid)
        user = request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, uuid):
        """Add request.user to the voters queryset of an answer instance."""
        answer = get_object_or_404(Answer, uuid=uuid)
        rating = request.data.get("rating")
        user = request.user
        if rating == "upvote":
            answer.upvotes.add(user)
        else:
            answer.downvotes.add(user)

        answer.save()
        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentCreateAPIView(CreateAPIView):
    """Allow users to add a comment to an answer instance."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        answer = get_object_or_404(Answer, uuid=self.request.data.get("answer"))

        serializer.save(author=request_user, answer=answer)


class RetrieveUpdateDestroyCommentAPIView(RetrieveUpdateDestroyAPIView):
    """Provide *RUD functionality for a comment instance to it's author."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "uuid"
