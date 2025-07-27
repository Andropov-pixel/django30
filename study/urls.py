from django.urls import path
from rest_framework.routers import DefaultRouter

from study.views import (CourseViewSet, LessonCreateAPIView,
                         LessonDestroyAPIView, LessonListAPIView,
                         LessonRetrieveAPIView, LessonUpdateAPIView,
                         SubscriptionCreateAPIView)

app_name = "study"

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path(
        "course/subscription/",
        SubscriptionCreateAPIView.as_view(),
        name="course_subscription",
    ),
] + router.urls