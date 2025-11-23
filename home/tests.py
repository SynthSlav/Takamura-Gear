from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.
class HomeViewsTest(TestCase):
    """Test cases for home views"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_home_page_loads(self):
        """Test home page loads successfully"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

    def test_home_page_contains_hero(self):
        """Test home page contains hero section"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "GEAR UP FOR VICTORY")

    def test_home_page_contains_categories(self):
        """Test home page shows category cards"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Gloves")
        self.assertContains(response, "Fight Gear")
        self.assertContains(response, "Protective Equipment")

    def test_home_page_contains_features(self):
        """Test home page shows feature section"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Free Delivery")
        self.assertContains(response, "Quality Guaranteed")
