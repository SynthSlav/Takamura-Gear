from decimal import Decimal
from django.conf import settings
from products.models import Product


def cart_contents(request):
    """Make cart contents available across all templates"""

    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get("cart", {})

    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            # Product has no size
            product = Product.objects.get(pk=item_id)
            total += item_data * product.price
            product_count += item_data
            cart_items.append(
                {
                    "item_id": item_id,
                    "quantity": item_data,
                    "product": product,
                }
            )
        else:
            # Product has sizes
            product = Product.objects.get(pk=item_id)
            for size, quantity in item_data["items_by_size"].items():
                total += quantity * product.price
                product_count += quantity
                cart_items.append(
                    {
                        "item_id": item_id,
                        "quantity": quantity,
                        "product": product,
                        "size": size,
                    }
                )

    # Delivery calculation
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = settings.STANDARD_DELIVERY_COST
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        "cart_items": cart_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "grand_total": grand_total,
    }

    return context
