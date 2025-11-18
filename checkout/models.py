import uuid
from django.db import models

# Create your models here.


class Order(models.Model):
    """
    Store customer order information
    """

    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
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

    def save(self, *args, **kwargs):
        """Override save to set order number if not already set"""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
