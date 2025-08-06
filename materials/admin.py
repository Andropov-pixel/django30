from django.contrib import admin

from materials.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админка курса."""

    list_display = ("id", "name", "description", "image")
    search_fields = ("name",)
    search_filter = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Админка урока."""

    list_display = ("id", "title", "description", "preview", "video_link")
    search_fields = ("name",)
    search_filter = ("name",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админка подписки."""

    list_display = ("id", "user", "course")
    search_fields = ("user",)
    search_filter = ("user",)
