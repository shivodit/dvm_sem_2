
from django.urls import path
from django.shortcuts import render
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [

    # Auth views
    path('accounts/customer_register/',views.customerRegisterView.as_view(),name="customer_register"),
    path('accounts/seller_register/',views.sellerRegisterView.as_view(),name="seller_register"),
    path('accounts/login/',LoginView.as_view(template_name='users/login.html'),name="login"),
    path('accounts/logout/',LogoutView.as_view(next_page='dashboard'),name="logout"),
    
]