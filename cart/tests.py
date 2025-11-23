from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category

# Create your tests here.


class CartViewsTest(TestCase):
    """Test cases for cart views"""

    def setUp(self):
        """Set up test client and create test product"""
        self.client = Client()
        self.category = Category.objects.create(name="gloves", friendly_name="Gloves")
        self.product = Product.objects.create(
            category=self.category,
            sku="tg-test-001",
            name="Test Boxing Gloves",
            description="Test description",
            price=49.99,
            has_sizes=True,
        )
        self.product_no_size = Product.objects.create(
            category=self.category,
            sku="tg-test-002",
            name="Test Mouthguard",
            description="Test description",
            price=12.99,
            has_sizes=False,
        )

    def test_view_cart_empty(self):
        """Test viewing empty cart"""
        response = self.client.get(reverse("view_cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")
        self.assertContains(response, "Your cart is empty")

    def test_add_product_to_cart_no_size(self):
        """Test adding a product without size to cart"""
        response = self.client.post(
            reverse("add_to_cart", args=[self.product_no_size.id]),
            {
                "quantity": 1,
                "redirect_url": reverse(
                    "product_detail", args=[self.product_no_size.id]
                ),
            },
        )
        # Should redirect after adding
        self.assertEqual(response.status_code, 302)
        # Check cart in session
        cart = self.client.session.get("cart", {})
        self.assertIn(str(self.product_no_size.id), cart)

    def test_add_product_to_cart_with_size(self):
        """Test adding a product with size to cart"""
        response = self.client.post(
            reverse("add_to_cart", args=[self.product.id]),
            {
                "quantity": 1,
                "product_size": "12oz",
                "redirect_url": reverse("product_detail", args=[self.product.id]),
            },
        )
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get("cart", {})
        self.assertIn(str(self.product.id), cart)

    def test_add_multiple_quantities(self):
        """Test adding multiple quantities of same product"""
        self.client.post(
            reverse("add_to_cart", args=[self.product_no_size.id]),
            {"quantity": 3, "redirect_url": reverse("view_cart")},
        )
        cart = self.client.session.get("cart", {})
        self.assertEqual(cart[str(self.product_no_size.id)], 3)

    def test_update_cart_quantity(self):
        """Test updating quantity in cart"""
        # First add item to cart
        self.client.post(
            reverse("add_to_cart", args=[self.product_no_size.id]),
            {"quantity": 1, "redirect_url": reverse("view_cart")},
        )
        # Then update quantity
        response = self.client.post(
            reverse("update_cart", args=[self.product_no_size.id]), {"quantity": 5}
        )
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get("cart", {})
        self.assertEqual(cart[str(self.product_no_size.id)], 5)

    def test_remove_from_cart(self):
        """Test removing item from cart"""
        # First add item
        self.client.post(
            reverse("add_to_cart", args=[self.product_no_size.id]),
            {"quantity": 1, "redirect_url": reverse("view_cart")},
        )
        # Then remove it
        response = self.client.post(
            reverse("remove_from_cart", args=[self.product_no_size.id])
        )
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get("cart", {})
        self.assertNotIn(str(self.product_no_size.id), cart)


class CartContextTest(TestCase):
    """Test cart context processor calculations"""

    def setUp(self):
        """Set up test client and products"""
        self.client = Client()
        self.category = Category.objects.create(
            name="equipment", friendly_name="Equipment"
        )
        self.product = Product.objects.create(
            category=self.category,
            sku="tg-test-003",
            name="Test Bag",
            description="Test description",
            price=100.00,
            has_sizes=False,
        )

    def test_cart_total_calculation(self):
        """Test cart totals are calculated correctly"""
        # Add product to cart
        self.client.post(
            reverse("add_to_cart", args=[self.product.id]),
            {"quantity": 2, "redirect_url": reverse("view_cart")},
        )
        response = self.client.get(reverse("view_cart"))
        # 2 x £100 = £200, over £99 threshold so free delivery
        self.assertContains(response, "200.00")

    def test_delivery_threshold(self):
        """Test free delivery threshold works"""
        self.product_cheap = Product.objects.create(
            category=self.category,
            sku="tg-test-004",
            name="Test Wraps",
            description="Test description",
            price=10.00,
            has_sizes=False,
        )
        # Add cheap product - under £99 threshold
        self.client.post(
            reverse("add_to_cart", args=[self.product_cheap.id]),
            {"quantity": 1, "redirect_url": reverse("view_cart")},
        )
        response = self.client.get(reverse("view_cart"))
        # Should show delivery message
        self.assertContains(response, "more for free delivery")
