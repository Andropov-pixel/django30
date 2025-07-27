from django.contrib.auth.models import AbstractUser
from django.db import models

from study.models import Course, Lesson


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите вашу электронную почту. Используется для входа в систему.",
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Укажите ваш контактный номер телефона (необязательно).",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите название города проживания (необязательно).",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите изображение для профиля (необязательно).",
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="Группы, к которым принадлежит этот пользователь. Пользователь получит все разрешения, предоставленные каждой из своих групп.",
        verbose_name="Группы",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Специфические разрешения для этого пользователя.",
        verbose_name="Разрешения пользователя",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_date = models.DateField(null=True, blank=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Оплаченный курс",
        null=True,
        blank=True,
    )
    separately_paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Оплаченный урок",
        null=True,
        blank=True,
    )
    payment_amount = models.PositiveIntegerField(
        default=0, verbose_name="Сумма оплаты", null=True, blank=True
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
        default="cash",
        verbose_name="Вариант оплаты",
        null=True,
        blank=True,
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="Id сессии",
        help_text="Введите Id сессии",
        null=True,
        blank=True,
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Ссылка на оплату товара",
        help_text="Введите на оплату товара",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.email} - {self.paid_course or self.separately_paid_lesson} ({self.payment_amount} руб.)"

    class Meta:
        verbose_name = "Pay"
        verbose_name_plural = "Pays"