from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Category, Product, Store

ROLE_CHOICES = (
    ("customer", "Customer"),
    ("seller", "Seller"),
)


class SignUpForm(UserCreationForm):
    """Registration form. The user picks whether they are a customer or a seller."""

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    phone = forms.CharField(
        max_length=20, required=False, help_text="Only needed for customers"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role", "phone"]


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name", "description"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "image", "stock", "category"]


class AddBalanceForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=1)
