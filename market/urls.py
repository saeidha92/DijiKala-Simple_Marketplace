from django.urls import path
from . import views

app_name = "market"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("", views.home_view, name="home"),
    path("stores/", views.stores_view, name="stores"),
    path("stores/<int:pk>/", views.store_detail_view, name="store_detail"),
]



