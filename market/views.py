from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddBalanceForm, ProductForm, SignUpForm, StoreForm
from .models import (
    Category,
    CartItem,
    CustomerProfile,
    Order,
    OrderItem,
    Product,
    SellerProfile,
    Store,
)



# Small helpers
# ---------------------------------------------------------------------------

def is_seller(user):
    return hasattr(user, "seller_profile")


def is_customer(user):
    return hasattr(user, "customer_profile")

