from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from materials.tasks import send_information_about_course_update
from users.permissions import IsModer, IsOwner


@method_decorator(
    name="list", decorator=swagger_auto_schema(operation_description="Course ViewSet")
)
class CourseViewSet(ModelViewSet):
    """Course ViewSet."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        """Ограничивает доступ модератору"""
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perfom_update(self, serializer):
        """Dызов задачи на отправку сообщения об обновлении курса"""
        course = serializer.save()
        send_information_about_course_update.delay(course.id)


class LessonCreateAPIView(CreateAPIView):
    """Lesson Create."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """Lesson List."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    """Lesson Retrieve."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    """Lesson Update."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    """Lesson Destroy."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer | IsOwner]


class SubscriptionView(APIView):
    """Subscription View."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user  # получаем пользователя
        course_id = request.data.get("course_id")  # получаем id курса
        course_item = get_object_or_404(
            Course, id=course_id
        )  # получаем объект курса из базы

        # получаем объекты подписок по текущему пользователю и курса
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"

        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        # Возвращаем ответ в API
        return Response({"message": message}, status=status.HTTP_200_OK)
