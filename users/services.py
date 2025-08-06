import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    """Создание продукта в stripe."""
    product = stripe.Product.create(name=course.name)
    return product


def create_stripe_price(amount, product_id):
    """Создание цены в stripe."""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product_id,
    )
    return price


def create_stripe_sessions(price_id):
    """Создание сессии в stripe."""
    sessions = stripe.checkout.Session.create(
        payment_method_types=["card"],
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return sessions.get("id"), sessions.get("url")
