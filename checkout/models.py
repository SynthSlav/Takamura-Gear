import uuid
from django.db import models
from products.models import Product
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

# Create your models here.


class Order(models.Model):
    """
    Store customer order information
    """

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        "profiles.UserProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label="Country *", null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    delivery_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
    )
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
    )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
    )

    def _generate_order_number(self):
        """Generate random unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs
        """
        self.order_total = (
            self.lineitems.aggregate(Sum("lineitem_total"))["lineitem_total__sum"] or 0
        )

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = settings.STANDARD_DELIVERY_COST
        else:
            self.delivery_cost = 0

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """Override save to set order number if not already set"""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Individual item in an order
    Represents one product (with optional size) and quantity
    """

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    product_size = models.CharField(max_length=10, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override save to calculate lineitem total
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SKU {self.product.sku} on order {self.order.order_number}"
