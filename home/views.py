from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


def index(request):
    """View to return the index page"""

    # Handle newsletter subscription
    if request.method == "POST" and "email" in request.POST:
        email = request.POST.get("email")
        messages.success(
            request,
            f"Thank you for subscribing! We'll keep you updated with exclusive deals and promotions at {email}",
        )
        return redirect("home")

    return render(request, "home/index.html")
