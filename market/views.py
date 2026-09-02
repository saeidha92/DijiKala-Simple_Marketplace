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

# Auth
# ---------------------------------------------------------------------------

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data["role"]
            if role == "seller":
                SellerProfile.objects.create(user=user)
            else:
                CustomerProfile.objects.create(
                    user=user, phone=form.cleaned_data.get("phone", "")
                )
            login(request, user)
            messages.success(request, "Welcome to DijiKala! Your account was created.")
            return redirect("market:home")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


