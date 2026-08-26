from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Prefetch
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.cache import cache_page
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.documents import CustomUserDocument
from accounts.models import CustomUser
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    AnswerSerializer,
    CommentSerializer,
    CustomTokenObtainPairSerializer,
    CustomUserDocumentSerializer,
    CustomUserSerializer,
    NotificationSerializer,
    ProfileSerializer,
    QuestionSerializer,
    TagSerializer,
    UserDetailSerializer,
)
from core.models import Answer, Comment, Notification, Question, Tag
from core.tasks import (
    task_publish_answer_notification,
    task_publish_comment_notification,
    task_publish_follow_event,
    task_publish_login_event,
    task_publish_profile_update_event,
)

QUESTION_LIST_CACHE_KEY = "question_list"


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        task_publish_login_event.delay(serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ListCustomUsersApiView(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["username", "email"]
    ordering_fields = ["username", "email"]
    search_fields = ["username", "email"]


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        task_publish_profile_update_event.delay(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailApiView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    def get_queryset(self):
        return CustomUser.objects.prefetch_related(
            "followers", "following", "questions"
        ).annotate(questions_count=Count("questions"))


class CustomUserDocumentView(DocumentViewSet):
    document = CustomUserDocument
    serializer_class = CustomUserDocumentSerializer
    permission_classes = []

    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = {
        "username": {"fuzziness": "AUTO"},
        "email": {"fuzziness": "AUTO"},
        "firstName": None,
        "lastName": None,
    }

    filter_fields = {
        "email": "email.raw",
        "username": "username.raw",
        "is_staff": "is_staff",
        "is_superuser": "is_superuser",
    }

    ordering_fields = {
        "id": "id",
        "email": "email.raw",
        "username": "username.raw",
    }
    ordering = ("id",)


class FollowUserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user = request.user
        followed_user = get_object_or_404(CustomUser, username=username)

        if user == followed_user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.following.add(followed_user)
        followed_user.followers.add(user)

        task_publish_follow_event.delay(
            event_type="user.followed",
            follower_id=user.id,
            followed_user_id=followed_user.id,
        )

        return Response(
            {"detail": f"Now following {username}"}, status=status.HTTP_200_OK
        )

    def delete(self, request, username):
        user = request.user
        followed_user = get_object_or_404(CustomUser, username=username)

        user.following.remove(followed_user)
        followed_user.followers.remove(user)

        # Fixed: now offloaded via Celery task
        task_publish_follow_event.delay(
            event_type="user.unfollowed",
            follower_id=user.id,
            followed_user_id=followed_user.id,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not user.check_password(current_password):
            return Response(
                {"message": "Your current password is not correct!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        image = request.FILES.get("image")

        if not image:
            return Response(
                {"message": "No image provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if image.size > 3 * 1024 * 1024:  # 3MB
            return Response(
                {"message": "Image size should not exceed 3MB!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.profilePicture:
            user.profilePicture.delete(save=False)

        user.profilePicture = image
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateQuestionsApiView(ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["content", "author__email"]
    ordering_fields = ["created_at", "updated_at"]
    search_fields = ["content", "author__email"]

    def get_queryset(self):
        return (
            Question.objects.select_related("author")
            .prefetch_related(
                "upvotes",
                "downvotes",
                "tags",
                Prefetch(
                    "answers",
                    queryset=Answer.objects.select_related(
                        "author", "question"
                    ).prefetch_related("upvotes", "downvotes", "comments"),
                ),
            )
            .annotate(answers_count=Count("answers"))
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, slug=slugify(serializer.validated_data["content"])
        )
        cache.delete_pattern(f"*{QUESTION_LIST_CACHE_KEY}*")

    @method_decorator(cache_page(60 * 10, key_prefix=QUESTION_LIST_CACHE_KEY))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class RetrieveUpdateDestroyQuestionApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Question.objects.select_related("author")
            .prefetch_related(
                "upvotes",
                "downvotes",
                "tags",
                Prefetch(
                    "answers",
                    queryset=Answer.objects.select_related(
                        "author", "question"
                    ).prefetch_related(
                        "upvotes",
                        "downvotes",
                        Prefetch(
                            "comments",
                            queryset=Comment.objects.select_related("author"),
                        ),
                    ),
                ),
            )
            .annotate(answers_count=Count("answers"))
        )

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
        return (
            Question.objects.filter(author=self.request.user)
            .select_related("author")
            .prefetch_related(
                "upvotes",
                "downvotes",
                "tags",
                Prefetch(
                    "answers",
                    queryset=Answer.objects.select_related("author").prefetch_related(
                        "upvotes", "downvotes"
                    ),
                ),
            )
            .annotate(answers_count=Count("answers"))
            .order_by("-created_at")
        )


class QuestionLikeAPIView(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        user = request.user
        question.upvotes.remove(user)
        question.downvotes.remove(user)
        question.save()

        serializer = self.serializer_class(question, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        rating = request.data.get("rating")
        user = request.user

        if rating == "upvote":
            question.downvotes.remove(user)
            question.upvotes.add(user)
        else:
            question.upvotes.remove(user)
            question.downvotes.add(user)

        question.save()
        serializer = self.serializer_class(question, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerCreateAPIView(CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        question = get_object_or_404(Question, slug=self.kwargs.get("slug"))

        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question!")

        answer = serializer.save(author=request_user, question=question)

        task_publish_answer_notification.delay(
            answer_id=answer.id,
            question_id=question.id,
            author_id=request_user.id,
        )


class AnswerRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "uuid"


class MyAnswersListAPIView(ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Answer.objects.filter(author=self.request.user)
            .select_related("author", "question")
            .prefetch_related(
                "upvotes",
                "downvotes",
                Prefetch("comments", queryset=Comment.objects.select_related("author")),
            )
            .annotate(comments_count=Count("comments"))
            .order_by("-created_at")
        )


class AnswerListAPIView(ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Answer.objects.filter(question__slug=self.kwargs.get("slug"))
            .select_related("author", "question")
            .prefetch_related(
                "upvotes",
                "downvotes",
                Prefetch("comments", queryset=Comment.objects.select_related("author")),
            )
            .annotate(comments_count=Count("comments"))
            .order_by("-created_at")
        )


class AnswerLikeAPIView(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, uuid):
        answer = get_object_or_404(Answer, uuid=uuid)
        user = request.user
        answer.upvotes.remove(user)
        answer.downvotes.remove(user)
        answer.save()

        serializer = self.serializer_class(answer, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, uuid):
        answer = get_object_or_404(Answer, uuid=uuid)
        rating = request.data.get("rating")
        user = request.user

        if rating == "upvote":
            answer.downvotes.remove(user)
            answer.upvotes.add(user)
        else:
            answer.upvotes.remove(user)
            answer.downvotes.add(user)

        answer.save()
        serializer = self.serializer_class(answer, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        answer = get_object_or_404(Answer, uuid=self.request.data.get("answer"))

        comment = serializer.save(author=request_user, answer=answer)

        # Trigger Celery comment notification task
        task_publish_comment_notification.delay(
            comment_id=comment.id,
            answer_id=answer.id,
            author_id=request_user.id,
        )


class RetrieveUpdateDestroyCommentAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "uuid"


class ListCreateTagsApiView(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["name"]
    ordering_fields = ["name"]
    search_fields = ["name"]


class RetrieveUpdateDestroyTagApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


class ListNotificationsApiView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Notification.objects.filter(recipient=self.request.user)
            .select_related("recipient")
            .order_by("-created_at")
        )