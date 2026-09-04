from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import CustomerProfile, Product, SellerProfile, Store


class MarketplaceFlowTests(TestCase):
    """Basic end-to-end tests for the seller and customer flows."""

    def setUp(self):
        seller_user = User.objects.create_user(username="seller", password="pass12345")
        self.seller_profile = SellerProfile.objects.create(user=seller_user)
        self.store = Store.objects.create(
            name="Demo Store", owner=self.seller_profile, description="test"
        )
        self.product = Product.objects.create(
            name="Keyboard", price=Decimal("25.00"), store=self.store, stock=3
        )

        customer_user = User.objects.create_user(username="customer", password="pass12345")
        self.customer_profile = CustomerProfile.objects.create(
            user=customer_user, balance=Decimal("100.00")
        )

    def test_home_page_lists_products(self):
        response = self.client.get(reverse("market:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Keyboard")

    def test_customer_can_add_to_cart_and_checkout(self):
        self.client.login(username="customer", password="pass12345")
        self.client.get(reverse("market:add_to_cart", args=[self.product.id]))
        response = self.client.post(reverse("market:checkout"), follow=True)
        self.assertEqual(response.status_code, 200)

        self.customer_profile.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(self.customer_profile.balance, Decimal("75.00"))
        self.assertEqual(self.product.stock, 2)

    def test_seller_can_create_store(self):
        self.client.login(username="seller", password="pass12345")
        response = self.client.post(
            reverse("market:create_store"),
            {"name": "Second Store", "description": "more stuff"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Store.objects.filter(name="Second Store").exists())

    def test_customer_cannot_access_seller_panel(self):
        self.client.login(username="customer", password="pass12345")
        response = self.client.get(reverse("market:seller_panel"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "seller_panel.html")

    def test_store_balance_credited_on_checkout(self):
        self.client.login(username="customer", password="pass12345")
        self.client.get(reverse("market:add_to_cart", args=[self.product.id]))
        self.client.post(reverse("market:checkout"), follow=True)
        self.store.refresh_from_db()
        self.assertEqual(self.store.balance, Decimal("25.00"))
