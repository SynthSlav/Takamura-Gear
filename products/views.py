from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Create your views here.


def all_products(request):
    """Show all products"""
    products = Product.objects.all()

    # Filter by category if provided
    category = request.GET.get("category")
    if category:
        products = products.filter(category__name=category)
        current_category = Category.objects.get(name=category)

    # Sort products
    sort = request.GET.get("sort", "name")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "name":
        products = products.order_by("name")

    context = {
        "products": products,
        "current_category": current_category,
        "current_sort": sort,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """Show individual product details"""
    product = get_object_or_404(Product, pk=product_id)
    context = {"product": product}
    return render(request, "products/product_detail.html", context)
