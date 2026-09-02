from django.urls import path
from . import views

app_name = "market"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("", views.home_view, name="home"),
    path("stores/", views.stores_view, name="stores"),
    path("stores/<int:pk>/", views.store_detail_view, name="store_detail"),
    path("seller/", views.seller_panel_view, name="seller_panel"),
    path("seller/store/create/", views.create_store_view, name="create_store"),
    path("seller/store/<int:store_id>/add-product/", views.add_product_view, name="add_product"),
    path("customer/", views.customer_panel_view, name="customer_panel"),
    path("payment/", views.payment_view, name="payment"),
]



