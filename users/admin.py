from django.contrib import admin

from users.models import Payments, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка пользователя."""

    list_display = ("id", "email", "first_name", "last_name", "phone", "city", "avatar")


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    """Админка оплаты курса."""

    list_display = (
        "id",
        "user",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "payment_amount",
        "payment_method",
    )
    search_fields = ("user",)
    search_filter = (
        "payment_date",
        "paid_course",
        "paid_lesson",
    )
