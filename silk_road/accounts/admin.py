from django.contrib import admin

# Register your models here.
from .models import Seller, Customer, User

admin.site.register([Seller,Customer,User])