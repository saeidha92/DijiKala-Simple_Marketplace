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


# Customer area
# ---------------------------------------------------------------------------

@login_required
def customer_panel_view(request):
    if not is_customer(request.user):
        messages.error(request, "Only customers can access the customer panel.")
        return redirect("market:home")
    profile = request.user.customer_profile
    return render(request, "customer_panel.html", {"profile": profile})

@login_required
def payment_view(request):
    if not is_customer(request.user):
        messages.error(request, "Only customers can add balance.")
        return redirect("market:home")
    profile = request.user.customer_profile
    if request.method == "POST":
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            profile.balance += form.cleaned_data["amount"]
            profile.save()
            messages.success(request, f'{form.cleaned_data["amount"]} was added to your balance.')
            return redirect("market:customer_panel")
    else:
        form = AddBalanceForm()
    return render(request, "payment.html", {"form": form, "profile": profile})

# Cart
# ---------------------------------------------------------------------------


@login_required
def add_to_cart_view(request, product_id):
    if not is_customer(request.user):
        messages.error(request, "Only customers can use the cart.")
        return redirect("market:home")
    product = get_object_or_404(Product, pk=product_id)
    item, created = CartItem.objects.get_or_create(
        product=product, customer=request.user.customer_profile
    )
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{product.name}" was added to your cart.')
    return redirect(request.META.get("HTTP_REFERER", "market:home"))


@login_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, customer=request.user.customer_profile)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("market:cart")


@login_required
def cart_view(request):
    if not is_customer(request.user):
        messages.error(request, "Only customers can use the cart.")
        return redirect("market:home")
    profile = request.user.customer_profile
    items = profile.cart_items.select_related("product", "product__store")
    total = sum((item.total_price() for item in items), Decimal("0"))
    return render(request, "cart.html", {"items": items, "total": total})


@login_required
@transaction.atomic
def checkout_view(request):
    if not is_customer(request.user):
        messages.error(request, "Only customers can checkout.")
        return redirect("market:home")
    profile = request.user.customer_profile
    items = list(profile.cart_items.select_related("product", "product__store__owner"))

    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("market:cart")

    total = sum((item.total_price() for item in items), Decimal("0"))
    if profile.balance < total:
        messages.error(request, "Not enough balance. Please add funds first.")
        return redirect("market:payment")

    order = Order.objects.create(customer=profile, total_amount=total)
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )
        # Demo logic: money "moves" from the customer to the seller's store.
        item.product.stock = max(item.product.stock - item.quantity, 0)
        item.product.save()

        store = item.product.store
        store.balance += item.total_price()
        store.save()

    profile.balance -= total
    profile.save()
    item_ids = [item.id for item in items]
    CartItem.objects.filter(id__in=item_ids).delete()

    messages.success(request, "Checkout complete! Thank you for your order.")
    return render(request, "thank_you.html", {"order": order})


# -----------------------------------------

@login_required
def order_history_view(request):
    if not is_customer(request.user):
        messages.error(request, "Only customers have an order history.")
        return redirect("market:home")
    orders = request.user.customer_profile.orders.prefetch_related("items")
    return render(request, "order_history.html", {"orders": orders})




