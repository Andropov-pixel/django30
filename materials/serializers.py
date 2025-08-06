from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока."""

    video_link = serializers.URLField(validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса."""

    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(
        many=True, read_only=True
    )  # Выдает и количество уроков курса и информацию по всем урокам курса одновременно
    is_subscription = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        """Получает объект курса obj и возвращает количество связанных уроков"""
        return obj.lessons.count()  # Используем related_name 'lessons'

    def get_is_subscription(self, obj):
        """Проверяет наличие подписки."""
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = [
            "name",
            "lesson_count",
            "lessons",
            "is_subscription",
        ]  # указанные здесь поля будут возвращаться в postman
