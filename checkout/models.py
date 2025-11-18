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
    date = models.DateTimeField(auto_now_add=True)

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
