from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

class Seller(models.Model):
    cuser = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True , null = True
    )
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return self.company_name

class Customer(models.Model):
    cuser = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True, blank=True
    )   
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    wallet_balance = models.FloatField()

    def __str__(self) -> str:
        return self.cuser.username
