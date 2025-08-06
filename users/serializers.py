from rest_framework import serializers

from users.models import Payments, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализатор оплаты."""

    class Meta:
        model = Payments
        fields = "__all__"
