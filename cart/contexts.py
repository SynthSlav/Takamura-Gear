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
        product = Product.objects.get(pk=item_id)

        if isinstance(item_data, int):
            # Product has no size
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
            # Product has size
            quantity = item_data["quantity"]
            size = item_data["size"]
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

    context = {
        "cart_items": cart_items,
        "total": total,
        "product_count": product_count,
    }

    return context
