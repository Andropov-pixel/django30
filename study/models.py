from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(
        max_length=160,
        verbose_name="Название курса",
        help_text="Введите название курса (до 160 символов).",
    )
    preview_img = models.ImageField(
        upload_to="course_previews/",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Загрузите изображение для превью (необязательно).",
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите подробное описание курса."
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        blank=True,
        null=True,
        verbose_name="Владелец курса",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.title} {self.description}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Выберите курс, к которому относится данный урок.",
    )
    title = models.CharField(
        max_length=160,
        verbose_name="Название урока",
        help_text="Введите название урока (до 160 символов).",
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Введите подробное описание урока."
    )
    preview_img = models.ImageField(
        upload_to="lesson_previews/",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Загрузите изображение для превью урока (необязательно).",
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Введите URL-адрес видео для урока (необязательно).",
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        blank=True,
        null=True,
        verbose_name="Владелец курса",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.course} {self.title}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"


class Subscription(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )
    sign_of_subscription = models.BooleanField(
        default=False,
        verbose_name="Характер подписки",
    )

    def __str__(self):
        return f"{self.user} {self.course}"

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"