from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription
from users.models import User


@shared_task
def send_information_about_course_update(course_id):
    """Отправляет сообщение пльзователю о подписке."""
    subject = "Обновление курса!"
    message = "Информируем Вас о том, что материалы курса обновлены!"
    subscription = Subscription.objects.filter(course_id=course_id)
    for s in subscription:
        send_mail(subject, message, EMAIL_HOST_USER, [s.user.email])


@shared_task
def blocking_user():
    """Проверяет пользователя по дате последнего входа."""
    month_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_user = User.objects.filter(last_login__lt=month_ago, is_active=True)
    inactive_user.update(is_active=False)
