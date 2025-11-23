from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category

# Create your tests here.


class CategoryModelTest(TestCase):
    """Test cases for the Category model"""

    def setUp(self):
        """Create a test category"""
        self.category = Category.objects.create(
            name="test_category", friendly_name="Test Category"
        )

    def test_category_string_representation(self):
        """Test category returns name as string"""
        self.assertEqual(str(self.category), "test_category")

    def test_category_friendly_name(self):
        """Test get_friendly_name method"""
        self.assertEqual(self.category.get_friendly_name(), "Test Category")


class ProductModelTest(TestCase):
    """Test cases for the Product model"""

    def setUp(self):
        """Create test category and product"""
        self.category = Category.objects.create(name="gloves", friendly_name="Gloves")
        self.product = Product.objects.create(
            category=self.category,
            sku="tg-test-001",
            name="Test Boxing Gloves",
            description="Test description for boxing gloves",
            has_sizes=True,
            price=49.99,
            rating=4.5,
        )

    def test_product_string_representation(self):
        """Test product returns name as string"""
        self.assertEqual(str(self.product), "Test Boxing Gloves")

    def test_product_has_category(self):
        """Test product is linked to category"""
        self.assertEqual(self.product.category.name, "gloves")

    def test_product_price(self):
        """Test product price is set correctly"""
        self.assertEqual(float(self.product.price), 49.99)


class ProductViewsTest(TestCase):
    """Test cases for product views"""

    def setUp(self):
        """Set up test client and create test data"""
        self.client = Client()
        self.category = Category.objects.create(name="gloves", friendly_name="Gloves")
        self.product = Product.objects.create(
            category=self.category,
            sku="tg-test-001",
            name="Test Boxing Gloves",
            description="Test description",
            price=49.99,
        )

    def test_all_products_view(self):
        """Test products page loads successfully"""
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

    def test_products_view_contains_product(self):
        """Test products page contains our test product"""
        response = self.client.get(reverse("products"))
        self.assertContains(response, "TEST BOXING GLOVES")

    def test_product_detail_view(self):
        """Test product detail page loads successfully"""
        response = self.client.get(reverse("product_detail", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")

    def test_product_detail_contains_product_info(self):
        """Test product detail page shows product information"""
        response = self.client.get(reverse("product_detail", args=[self.product.id]))
        self.assertContains(response, "Test Boxing Gloves")
        self.assertContains(response, "49.99")

    def test_category_filter(self):
        """Test filtering products by category"""
        response = self.client.get(reverse("products") + "?category=gloves")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TEST BOXING GLOVES")

    def test_price_sort_ascending(self):
        """Test sorting products by price ascending"""
        response = self.client.get(reverse("products") + "?sort=price_asc")
        self.assertEqual(response.status_code, 200)

    def test_price_sort_descending(self):
        """Test sorting products by price descending"""
        response = self.client.get(reverse("products") + "?sort=price_desc")
        self.assertEqual(response.status_code, 200)

    def test_invalid_product_returns_404(self):
        """Test accessing non-existent product returns 404"""
        response = self.client.get(reverse("product_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)
