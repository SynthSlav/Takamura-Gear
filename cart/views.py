from django.shortcuts import render, redirect, get_object_or_404
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
            cart[product_id]["quantity"] += quantity
        else:
            cart[product_id] = {"quantity": quantity, "size": size}
    else:
        # No size
        if product_id in list(cart.keys()):
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

    request.session["cart"] = cart
    messages.success(request, f"Added {product.name} to your cart")
    return redirect(redirect_url)
