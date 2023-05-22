from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from accounts.models import Customer, Seller
from .keyconfig import *
from mailjet_rest import Client
from django.shortcuts import render,redirect


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField( max_length=500)
    price = models.FloatField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f"media/images", max_length=None)
    quantity = models.IntegerField(default = 0) 

    def place_order(self,request,c,quantity):
        
        product=self
        cost = quantity * product.price
        # checks for valid order
        if cost <= c.wallet_balance and quantity <= product.quantity:
            order = Order(product=product,customer=c,quantity=quantity,cost=cost)
            order.save()
            c.wallet_balance -= cost
            product.quantity -= quantity
            product.save()
            c.save()
            # sending mail
            api_key = mailjet_api
            api_secret = mailjet_secret
            mailjet = Client(auth=(api_key, api_secret), version='v3')
            data = {
            'FromEmail': "f20221221@pilani.bits-pilani.ac.in",
            'FromName': "Silk Road | Merchant Support ",
            'Recipients': [
                {
                "Email": product.seller.cuser.email,
          
                "Name": product.seller.cuser.first_name
                }
            ],
            'Subject': f"New Order Recieved for {product.name}",
            'Text-part': "Dear passenger, welcome to Mailjet! May the delivery force be with you!",
            'Html-part': f"""<h5 >{ order.product.name }</h5>
                    <p >Quantity: { order.quantity }
                        <br/>Cost: { order.cost }
                        </p>
                        <hr/>
                    <p >Placed On: { order.order_date } at {order.order_time} by {order.customer.cuser.username}
                    <hr/>
                    This order has to be delivered to : {order.customer.address}
                    </p>
                    """
            }
            result = mailjet.send.create(data=data)
            print(result.status_code)
            print(result.json())
            #send mail 

            #TODO
            return 'success'
        else : 
            #TODO
            print('not valid request')

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_time = models.TimeField(auto_now_add=True)
    order_date = models.DateField(auto_now_add=True)
    cost = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity}-{self.product.name} by {self.customer.cuser.username}"

class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_wished = models.BooleanField(default=False)
    quantity = models.IntegerField()

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    customer_review = models.TextField(max_length=1000)
