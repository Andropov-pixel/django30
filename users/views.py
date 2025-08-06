from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_sessions)


class UserCreateAPIView(CreateAPIView):
    """CRUD для регистрации пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsViewSet(ModelViewSet):
    """Payments View."""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(CreateAPIView):
    """Оплата курса через stripe"""

    queryset = User.objects.all()
    serializer_class = PaymentsSerializer

    def post(self, request):
        course_id = request.data.get("course_id")
        amount = request.data.get("amount")
        course = Course.objects.get(id=course_id)

        product = create_stripe_product(course)
        price = create_stripe_price(amount, product.id)

        session_id, payment_link = create_stripe_sessions(price)

        return Response(
            {"session_id": session_id, "payment_Link": payment_link},
            status=status.HTTP_201_CREATED,
        )
