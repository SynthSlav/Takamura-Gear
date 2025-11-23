from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category
from checkout.models import Order, OrderLineItem
from profiles.models import UserProfile
from decimal import Decimal

# Create your tests here.


class OrderModelTest(TestCase):
    """Test cases for the Order model"""

    def setUp(self):
        """Create test order"""
        self.order = Order.objects.create(
            full_name="Test User",
            email="test@example.com",
            phone_number="07123456789",
            country="GB",
            town_or_city="London",
            street_address1="123 Test Street",
            delivery_cost=Decimal("5.99"),
            order_total=Decimal("50.00"),
            grand_total=Decimal("55.99"),
        )

    def test_order_number_generated(self):
        """Test order number is automatically generated"""
        self.assertIsNotNone(self.order.order_number)
        self.assertEqual(len(self.order.order_number), 32)

    def test_order_string_representation(self):
        """Test order returns order number as string"""
        self.assertEqual(str(self.order), self.order.order_number)


class OrderLineItemModelTest(TestCase):
    """Test cases for OrderLineItem model"""

    def setUp(self):
        """Create test order and line item"""
        self.category = Category.objects.create(name="gloves", friendly_name="Gloves")
        self.product = Product.objects.create(
            category=self.category,
            sku="tg-test-001",
            name="Test Boxing Gloves",
            description="Test description",
            price=Decimal("50.00"),
        )
        self.order = Order.objects.create(
            full_name="Test User",
            email="test@example.com",
            phone_number="07123456789",
            country="GB",
            town_or_city="London",
            street_address1="123 Test Street",
            delivery_cost=Decimal("0.00"),
            order_total=Decimal("100.00"),
            grand_total=Decimal("100.00"),
        )
        self.line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )

    def test_lineitem_total_calculated(self):
        """Test line item total is calculated correctly"""
        # 2 x £50 = £100
        self.assertEqual(self.line_item.lineitem_total, Decimal("100.00"))

    def test_lineitem_string_representation(self):
        """Test line item returns SKU and order number"""
        expected = f"SKU {self.product.sku} on order {self.order.order_number}"
        self.assertEqual(str(self.line_item), expected)


class CheckoutViewsTest(TestCase):
    """Test cases for checkout views"""

    def setUp(self):
        """Set up test client and create test data"""
        self.client = Client()
        self.category = Category.objects.create(name="gloves", friendly_name="Gloves")
        self.product = Product.objects.create(
            category=self.category,
            sku="tg-test-001",
            name="Test Boxing Gloves",
            description="Test description",
            price=Decimal("50.00"),
            has_sizes=False,
        )

    def test_checkout_empty_cart_redirect(self):
        """Test checkout redirects if cart is empty"""
        response = self.client.get(reverse("checkout"))
        # Should redirect to products page
        self.assertEqual(response.status_code, 302)

    def test_checkout_with_items_in_cart(self):
        """Test checkout page loads with items in cart"""
        # Add item to cart first
        self.client.post(
            reverse("add_to_cart", args=[self.product.id]),
            {"quantity": 1, "redirect_url": reverse("view_cart")},
        )
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout.html")

    def test_checkout_shows_cart_items(self):
        """Test checkout page displays cart items"""
        self.client.post(
            reverse("add_to_cart", args=[self.product.id]),
            {"quantity": 1, "redirect_url": reverse("view_cart")},
        )
        response = self.client.get(reverse("checkout"))
        self.assertContains(response, "Test Boxing Gloves")


class CheckoutSuccessViewTest(TestCase):
    """Test checkout success view"""

    def setUp(self):
        """Create test order"""
        self.client = Client()
        self.order = Order.objects.create(
            full_name="Test User",
            email="test@example.com",
            phone_number="07123456789",
            country="GB",
            town_or_city="London",
            street_address1="123 Test Street",
            delivery_cost=Decimal("5.99"),
            order_total=Decimal("50.00"),
            grand_total=Decimal("55.99"),
        )

    def test_checkout_success_page_loads(self):
        """Test checkout success page loads with valid order"""
        response = self.client.get(
            reverse("checkout_success", args=[self.order.order_number])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout_success.html")

    def test_checkout_success_displays_order_info(self):
        """Test checkout success shows order details"""
        response = self.client.get(
            reverse("checkout_success", args=[self.order.order_number])
        )
        self.assertContains(response, self.order.order_number)
        self.assertContains(response, "Test User")
