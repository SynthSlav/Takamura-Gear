from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Create your views here.


def all_products(request):
    """Show all products"""
    products = Product.objects.all()
    current_category = None
    # Filter by category if provided
    category = request.GET.get("category")
    if category:
        products = products.filter(category__name=category)
        current_category = Category.objects.get(name=category)

    # Filter by price range
    price_range = request.GET.get("price_range")
    if price_range == "under_30":
        products = products.filter(price__lt=30)
    elif price_range == "30_60":
        products = products.filter(price__gte=30, price__lt=60)
    elif price_range == "60_100":
        products = products.filter(price__gte=60, price__lt=100)
    elif price_range == "over_100":
        products = products.filter(price__gte=100)

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
        "current_price_range": price_range,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """Show individual product details"""
    product = get_object_or_404(Product, pk=product_id)
    context = {"product": product}
    return render(request, "products/product_detail.html", context)
