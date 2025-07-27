import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(instance):
    title_product = (
        f"{instance.paid_course}"
        if instance.paid_course
        else instance.separately_paid_lesson
    )
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.id


def create_stripe_price(payment, stripe_product_id):
    price = stripe.Price.create(
        currency="rub",
        unit_amount=payment.payment_amount * 100,
        product=stripe_product_id,
    )
    return price.id


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url