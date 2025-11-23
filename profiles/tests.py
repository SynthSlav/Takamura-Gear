from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile

# Create your tests here.


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        """Create test user - profile should auto-create via signal"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_profile_created_automatically(self):
        """Test profile is created when user is created"""
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_profile_string_representation(self):
        """Test profile returns username as string"""
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(profile), "testuser")

    def test_profile_default_fields_empty(self):
        """Test profile default fields are empty on creation"""
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsNone(profile.default_phone_number)
        self.assertIsNone(profile.default_town_or_city)


class UserProfileViewsTest(TestCase):
    """Test cases for profile views"""

    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_profile_page_requires_login(self):
        """Test profile page redirects if not logged in"""
        response = self.client.get(reverse("profile"))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_profile_page_loads_when_logged_in(self):
        """Test profile page loads for logged in user"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")

    def test_profile_page_shows_username(self):
        """Test profile page displays username"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertContains(response, "testuser")

    def test_profile_update(self):
        """Test updating profile information"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("profile"),
            {
                "default_full_name": "Test User",
                "default_phone_number": "07123456789",
                "default_street_address1": "123 Test Street",
                "default_town_or_city": "London",
                "default_postcode": "SW1A 1AA",
                "default_country": "GB",
            },
        )
        # Refresh profile from database
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.default_phone_number, "07123456789")
        self.assertEqual(profile.default_town_or_city, "London")


class ProfileOrderHistoryTest(TestCase):
    """Test order history display in profile"""

    def setUp(self):
        """Set up test client, user and order"""
        from checkout.models import Order
        from decimal import Decimal

        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.get(user=self.user)

        # Create a test order linked to profile
        self.order = Order.objects.create(
            user_profile=self.profile,
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

    def test_profile_shows_order_history(self):
        """Test profile page displays order history"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertContains(response, self.order.order_number[:10])
