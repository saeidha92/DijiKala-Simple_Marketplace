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


# Public pages
# ---------------------------------------------------------------------------


def home_view(request):
    products = Product.objects.select_related("store", "category").all()
    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)
    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(
        request,
        "home.html",
        {"products": products, "categories": categories, "query": query or ""},
    )


def stores_view(request):
    stores = Store.objects.select_related("owner__user").all()
    return render(request, "stores.html", {"stores": stores})


def store_detail_view(request, pk):
    store = get_object_or_404(Store, pk=pk)
    products = store.products.all()
    can_manage = (
        request.user.is_authenticated
        and is_seller(request.user)
        and store.owner.user == request.user
    )
    return render(
        request,
        "store_detail.html",
        {"store": store, "products": products, "can_manage": can_manage},
    )

# Seller area
# ---------------------------------------------------------------------------

@login_required
def seller_panel_view(request):
    if not is_seller(request.user):
        messages.error(request, "Only sellers can access the seller panel.")
        return redirect("market:home")
    stores = request.user.seller_profile.stores.all()
    return render(request, "seller_panel.html", {"stores": stores})


@login_required
def create_store_view(request):
    if not is_seller(request.user):
        messages.error(request, "Only sellers can create stores.")
        return redirect("market:home")
    if request.method == "POST":
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user.seller_profile
            store.save()
            messages.success(request, f'Store "{store.name}" was created.')
            return redirect("market:seller_panel")
    else:
        form = StoreForm()
    return render(request, "store_form.html", {"form": form})


@login_required
def add_product_view(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    if not is_seller(request.user) or store.owner.user != request.user:
        messages.error(request, "You do not have permission to manage this store.")
        return redirect("market:store_detail", pk=store.pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, f'Product "{product.name}" was added.')
            return redirect("market:store_detail", pk=store.pk)
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form, "store": store})

