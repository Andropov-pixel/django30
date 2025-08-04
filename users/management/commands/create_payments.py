from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):
    """Кастомная команда для создания платежей"""

    help = "Create sample payments"

    def handle(self, *args, **kwargs):
        user1 = User.objects.get(id=1)
        course1 = Course.objects.get(id=1)
        lesson1 = Lesson.objects.get(id=1)

        Payments.objects.create(
            user=user1,
            paid_course=course1,
            paid_lesson=lesson1,
            payment_amount=1000.00,
            payment_method="CASH",
        )

        self.stdout.write(self.style.SUCCESS("Successfully created payment records"))