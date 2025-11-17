from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_object_or_404,
    reverse,
    HttpResponse,
)
from django.contrib import messages
from products.models import Product

# Create your views here.


def view_cart(request):
    """Display the shopping cart"""
    return render(request, "cart/cart.html")


def add_to_cart(request, product_id):
    """Add a product to the shopping cart"""

    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    size = None

    if "product_size" in request.POST:
        size = request.POST["product_size"]

    cart = request.session.get("cart", {})

    if size:
        # Product has size
        if product_id in list(cart.keys()):
            if size in cart[product_id]["items_by_size"].keys():
                cart[product_id]["items_by_size"][size] += quantity
            else:
                cart[product_id]["items_by_size"][size] = quantity
        else:
            cart[product_id] = {"items_by_size": {size: quantity}}
    else:
        # No size
        if product_id in list(cart.keys()):
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

    request.session["cart"] = cart
    messages.success(request, f"Added {product.name} to your cart")
    return redirect(redirect_url)


def update_cart(request, product_id):
    """Update quantity of a product in the cart"""

    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity"))
    size = None

    if "product_size" in request.POST:
        size = request.POST["product_size"]

    cart = request.session.get("cart", {})

    if size:
        # Product has size
        if quantity > 0:
            cart[product_id]["items_by_size"][size] = quantity
            messages.success(
                request,
                f"Updated {product.name} ({size.upper()}) quantity to {quantity}",
            )
        else:
            del cart[product_id]["items_by_size"][size]
            if not cart[product_id]["items_by_size"]:
                cart.pop(product_id)
            messages.success(
                request, f"Removed {product.name} ({size.upper()}) from your cart"
            )
    else:
        # No size
        if quantity > 0:
            cart[product_id] = quantity
            messages.success(request, f"Updated {product.name} quantity to {quantity}")
        else:
            cart.pop(product_id)
            messages.success(request, f"Removed {product.name} from your cart")

    request.session["cart"] = cart
    return redirect(reverse("view_cart"))


def remove_from_cart(request, product_id):
    """Remove a product from the shopping cart"""

    try:
        product = get_object_or_404(Product, pk=product_id)
        size = None

        if "product_size" in request.POST:
            size = request.POST["product_size"]

        cart = request.session.get("cart", {})

        if size:
            # Product has size
            del cart[product_id]["items_by_size"][size]
            if not cart[product_id]["items_by_size"]:
                cart.pop(product_id)
            messages.success(
                request, f"Removed {product.name} ({size.upper()}) from your cart"
            )
        else:
            # No size
            cart.pop(product_id)
            messages.success(request, f"Removed {product.name} from your cart")

        request.session["cart"] = cart
        return redirect(reverse("view_cart"))

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return HttpResponse(status=500)
