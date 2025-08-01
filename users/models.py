from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from lms.models import Course, Lesson


class User(AbstractUser):
    """Модель: Пользователь"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")

    first_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Фамилия"
    )
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон"
    )
    country = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Страна"
    )
    photo = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Фото"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):

    CASH = "cash"
    TRANSFER = "transfer"

    METHOD_CHOICES = [(CASH, "Наличные"), (TRANSFER, "Перевод")]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_date = models.DateField(
        auto_now_add=True, verbose_name="Дата оплаты"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments_for_course",
        verbose_name="Курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments_for_lesson",
        verbose_name="Урок",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма платежа"
    )
    method = models.CharField(
        max_length=8,
        choices=METHOD_CHOICES,
        default=TRANSFER,
        verbose_name="Способ оплаты",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

class Subscription(models.Model):
        """Модель: Подписки"""

        user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
        date = models.DateTimeField(default=timezone.now,
                                    max_length=30, blank=True, null=True, verbose_name="Дата и время подписки")
        course = models.ForeignKey(Course, blank=True, null=True, verbose_name="Подписанный курс",
                                   on_delete=models.CASCADE, related_name="subscribes")

        def __str__(self):
            return f'{self.user} - {self.course or self.course}'