def cart_contents(request):
    """Make cart contents available across all templates"""

    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get("cart", {})

    context = {
        "cart_items": cart_items,
        "total": total,
        "product_count": product_count,
    }

    return context
