from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views as qv

router = DefaultRouter()
router.register(r"questions", qv.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register", qv.CreateCustomUserApiView.as_view(), name="signup"),
    path("login", qv.CustomTokenObtainPairView.as_view(), name="signin"),
    path("refresh", qv.TokenRefreshView.as_view(), name="refresh"),
    path(
        "questions-answers/<slug:slug>/",
        qv.AnswerListAPIView.as_view(),
        name="answer-list",
    ),
    path(
        "questions-new-answer/<slug:slug>/",
        qv.AnswerCreateAPIView.as_view(),
        name="answer-create",
    ),
    path(
        "answers-detail/<uuid:uuid>/",
        qv.AnswerRUDAPIView.as_view(),
        name="answer-detail",
    ),
    path(
        "answers-like/<uuid:uuid>/", qv.AnswerLikeAPIView.as_view(), name="answer-like"
    ),
]
