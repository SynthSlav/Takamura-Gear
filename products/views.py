from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ProductForm


# Create your views here.


def all_products(request):
    """Show all products"""
    products = Product.objects.all()
    current_category = None
    query = None
    # Filter by category if provided
    category = request.GET.get("category")
    if category:
        products = products.filter(category__name=category)
        current_category = Category.objects.get(name=category)

    # Search functionality
    if "q" in request.GET:
        query = request.GET["q"]
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse("products"))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)

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
    elif sort == "rating":
        products = products.order_by("-rating")
    elif sort == "name":
        products = products.order_by("name")

    context = {
        "products": products,
        "current_category": current_category,
        "current_sort": sort,
        "current_price_range": price_range,
        "search_term": query,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """Show individual product details"""
    product = get_object_or_404(Product, pk=product_id)
    context = {"product": product}
    return render(request, "products/product_detail.html", context)


# Admin views, only accessible by superusers


@login_required
def product_management(request):
    """Product management page - list all products (superuser only)"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    products = Product.objects.all()

    # Filter by category
    category = request.GET.get("category")
    if category:
        products = products.filter(category__name=category)

    products = products.order_by("name")

    template = "products/product_management.html"
    context = {
        "products": products,
    }

    return render(request, template, context)


@login_required
def add_product(request):
    """Add a product to the store (superuser only)"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request, "Failed to add product. Please ensure the form is valid."
            )
    else:
        form = ProductForm()

    template = "products/add_product.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """Edit a product in the store (superuser only)"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request, "Failed to update product. Please ensure the form is valid."
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You are editing {product.name}")

    template = "products/add_product.html"
    context = {
        "form": form,
        "product": product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a product from the store (superuser only)"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    product_name = product.name
    product.delete()
    messages.success(request, f"{product_name} has been removed from the database!")
    return redirect(reverse("product_management"))
