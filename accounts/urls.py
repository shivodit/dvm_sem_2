
from django.urls import path
from django.shortcuts import render
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [

    # Auth views
    path('customer_register/',views.customerRegisterView.as_view(),name="customer_register"),
    path('seller_register/',views.sellerRegisterView.as_view(),name="seller_register"),
    path('login/',LoginView.as_view(template_name='users/login.html'),name="login"),
    path('logout/',LogoutView.as_view(next_page='dashboard'),name="logout"),
    path('profile',views.profileMenu,name="profile_menu"),
    path('seller_profile/',views.sellerProfileView.as_view(),name="seller_profile_complete"),
    path('customer_profile/',views.customerProfileView.as_view(),name="customer_profile_complete"),

    
]