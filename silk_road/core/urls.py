from django.urls import path
from django.shortcuts import render
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    # customer view
    path('',lambda req : render(req,'index.html'),name="index"),
    path('home/',views.homeView.as_view(),name="home"),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('product_display/<pk>',views.productView,name="product_display"),
    path('buy_product/<pk>',views.buyProductView,name="buy_item"),
    path('add_balance/',views.addBalanceView.as_view(),name="add_balance"),
    path('customer_orders/',views.customerOrdersView,name='customer_orders'),
    path('vendor_profile/<pk>',views.vendorProfileView,name='vendor_profile'),
    path('customer_profile/',views.customerProfileView,name='customer_profile'),
    path('add_review/<pk>',views.addReview,name='add_review'),
    path('add_to_cart/<pk>/<is_wished>',views.addToCartView,name='add_to_cart'),
    path('show_cart_items/<is_wished>',views.showCartItemView,name='show_cart_items'),    
    path('remove_cart_item/<pk>',views.removeCartItem,name='remove_cart_item'),   
    path('buy_multiple_item/',views.buyMultiItemView,name='buy_multiple_item'),    
    path('order_detail/<pk>',views.orderDetailView,name='order_detail'),   

    # seller view
    path('seller/order_list/',views.listOrdersView,name="order_list"),
    path('seller/item_list/',views.listItemView,name="item_list"),
    path('seller/add_item/',views.addItemView.as_view(),name="add_item"),
    path('seller/delete_item/<pk>',views.deleteItemView,name = "delete_item"),
    path('seller/get_sales_report/',views.salesReportView,name = "get_sales_report"),
   
]