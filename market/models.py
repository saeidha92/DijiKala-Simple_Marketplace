from tkinter import CASCADE

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")

    def __str__(self):
        return f"Seller: {self.user.username}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    phone = models.CharField(max_length=20, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Customer: {self.user.username}"

class Store(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name="stores")
    description = models.TextField(blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("market:store_detail", args=[self.pk])

    








