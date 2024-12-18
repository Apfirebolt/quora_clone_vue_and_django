from django.urls import include, path

from api import views as apiViews


urlpatterns = [
    path("register", apiViews.CreateCustomUserApiView.as_view(), name="signup"),
    path("login", apiViews.CustomTokenObtainPairView.as_view(), name="signin"),
    path("refresh", apiViews.TokenRefreshView.as_view(), name="refresh"),
    path("profile", apiViews.ProfileView.as_view(), name="profile"),
    path("users", apiViews.ListCustomUsersApiView.as_view(), name="users"),
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
    # my questions list
    path(
        "my-questions",
        apiViews.MyQuestionsListAPIView.as_view(),
        name="my-questions",
    ),
    path(
        "questions-answers/<slug:slug>/",
        apiViews.AnswerListAPIView.as_view(),
        name="answer-list",
    ),
    # My answers list
    path(
        "my-answers",
        apiViews.MyAnswersListAPIView.as_view(),
        name="my-answers",
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
