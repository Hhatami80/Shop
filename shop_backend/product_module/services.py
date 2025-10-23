from .models import Order, OrderItem
from .models import Cart


def create_order(user):
    cart = user.cart
    if not cart.items.exists():
        raise ValueError("سبد خرید خالی است")

    order = Order.objects.create(user=user)

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.price,
        )

    order.calculate_total()
    cart.items.all().delete()

    return order
