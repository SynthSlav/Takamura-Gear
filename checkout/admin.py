from django.contrib import admin
from .models import Order

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model
    """

    list_display = (
        "order_number",
        "date",
        "full_name",
        "email",
    )

    ordering = ("-date",)


admin.site.register(Order, OrderAdmin)
