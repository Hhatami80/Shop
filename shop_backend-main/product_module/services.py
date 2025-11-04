from .models import Order, OrderItem
from .models import Cart


def create_order(user):
    cart = user.cart
    if not cart.items.exists():
        raise ValueError("سبد خرید خالی است")

    order = Order.objects.create(user=user)

    for item in cart.items.all():
        price = getattr(item.product, 'discounted_price', None) or item.product.price
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=price,
        )

    order.calculate_total()
    return order
