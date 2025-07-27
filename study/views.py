from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from study.models import Course, Lesson, Subscription
from study.paginators import CustomPagination
from study.serializers import (CourseDetailSerializers, CourseSerializers,
                               LessonSerializers, SubscriptionSerializer)
from study.tasks import course_update
from users.permissions import IsModerDRF, IsOwnerDRF


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializers
        return CourseSerializers

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerDRF,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerDRF | IsOwnerDRF,)
        elif self.action == "destroy":
            self.permission_classes = (IsModerDRF | IsOwnerDRF,)
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.save()
        course_update.delay(instance.pk)
        return instance


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializers
    permission_classes = (~IsModerDRF, IsAuthenticated)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = (IsModerDRF | IsOwnerDRF, IsAuthenticated)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = (IsModerDRF | IsOwnerDRF, IsAuthenticated)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (~IsModerDRF | IsOwnerDRF, IsAuthenticated)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Ваша подписка удалена!"
        else:
            Subscription.objects.create(
                user=user, course=course_item, sign_of_subscription=True
            )
            message = "Ваша подписка удалена!"
        return Response({"message": message})