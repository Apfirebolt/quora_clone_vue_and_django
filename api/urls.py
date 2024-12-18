from django.urls import include, path

from api import views as apiViews


urlpatterns = [
    path("register", apiViews.CreateCustomUserApiView.as_view(), name="signup"),
    path("login", apiViews.CustomTokenObtainPairView.as_view(), name="signin"),
    path("refresh", apiViews.TokenRefreshView.as_view(), name="refresh"),
    # questions create and list
    path(
        "questions",
        apiViews.ListCreateQuestionsApiView.as_view(),
        name="questions",
    ),
    # question detail
    path(
        "questions/<slug:slug>/",
        apiViews.RetrieveUpdateDestroyQuestionApiView.as_view(),
        name="question-detail",
    ),
    path(
        "questions-answers/<slug:slug>/",
        apiViews.AnswerListAPIView.as_view(),
        name="answer-list",
    ),
    path(
        "questions-new-answer/<slug:slug>/",
        apiViews.AnswerCreateAPIView.as_view(),
        name="answer-create",
    ),
    path(
        "answers-detail/<uuid:uuid>/",
        apiViews.AnswerRUDAPIView.as_view(),
        name="answer-detail",
    ),
    path(
        "answers-like/<uuid:uuid>/", apiViews.AnswerLikeAPIView.as_view(), name="answer-like"
    ),
]
