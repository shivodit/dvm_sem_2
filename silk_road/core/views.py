from typing import Any, Dict
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views import View, generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomerForm, SellerForm, CustomUserCreationForm, ProductForm
from .models import Product,Order,Seller,Review,Customer, CartItem
# Create your views here.
from allauth.account.views import SignupView
from allauth.account.forms import SignupForm
from .keyconfig import *
from mailjet_rest import Client
import csv
from django.http import HttpResponse
# oauth 
class ProfileSignupView(SignupView):

  template_name = 'register.html'
  success_url = '/'  # profile specific success url
  form_class = SignupForm
  profile_class = None  # profile class goes here

  def form_valid(self, form):
    response = super(ProfileSignupView, self).form_valid(form)
    profile = self.profile_class(user=self.user)
    profile.save()

    return response
  
class CustomerGoogleSignupView(ProfileSignupView):
   profile_class = Customer


class SellerGoogleSignupView(ProfileSignupView):
    profile_class = Seller

@login_required
def deleteItemView(request,pk):
    product = Product.objects.get(id=pk)
    if (product.seller != request.user.seller):
        raise PermissionDenied
    else :
        product.delete()
        return redirect('item_list')

class addItemView(LoginRequiredMixin,View):
    
    def get(self, request):
        if not request.user.is_seller :
            raise PermissionDenied()
        
        product_form = ProductForm()

        context = {
            'product_form' : product_form,
        }
        
        return render(request, 'sellers/add_item.html', context)
    
    def post(self,request):
        if not request.user.is_seller :
            raise PermissionDenied()
        
        product_form = ProductForm(
            request.POST,
            request.FILES
        )

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.seller = request.user.seller
            product.save()
            return redirect('item_list')
        
        else :
            context = {
                'product_form' : product_form,
            }
        
            return render(request, 'sellers/add_item.html', context)

@login_required
def listOrdersView(request):
    if request.user.is_seller:
        orders = Order.objects.filter(product__in=list(Product.objects.filter(seller=request.user.seller)))
        print(orders)
        return render(request,'customer/list_orders.html',{'orders':orders})
    else: 
        raise PermissionDenied


@login_required
def listItemView(request):
    if not request.user.is_seller:
        return redirect('home')
    
    items = request.user.seller.product_set.all()
    
    return render(request,'sellers/list_items.html',{'items':items})


@login_required
def dashboardView(request):
    if not request.user.is_seller:
        return redirect('home')
    
    n = Product.objects.filter(seller=request.user.seller).count()
    out_stock = Product.objects.filter(seller=request.user.seller,quantity=0).count()

    return render(request, 'dashboard.html', {'n':n,'out_stock':out_stock})


@login_required
def vendorProfileView(request,pk):

    seller = Seller.objects.get(pk=pk)
    items = seller.product_set.all()
    
    return render(request,'customer/vendor_profile.html',{'items':items,'seller':seller,'n':len(items)})

def salesReportView(request):
    orders = Order.objects.filter(product__in=list(Product.objects.filter(seller=request.user.seller)))
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Product', 'Ordered By', 'Date','Time', 'Quantity','Revenue'])
    for order in orders:
        writer.writerow([order.product.name, order.customer.cuser.username, order.order_date, order.order_time, order.quantity, order.cost])

    return response

@login_required
def customerProfileView(request):
    if request.method == 'GET':    
        if request.user.is_customer:
            customer = request.user.customer
            n = Order.objects.filter(customer=customer).count()
            return render(request,'customer/customer_profile.html',{'customer':customer,'n':n})
        else: 
            raise PermissionDenied
    
    elif request.method == 'POST':
        if request.user.is_customer:
            customer = request.user.customer
            add = request.POST['address']
            customer.address = add
            customer.save()  
            return redirect('customer_profile')
        else: 
            raise PermissionDenied
        
         
class homeView(LoginRequiredMixin,generic.ListView):

    model = Product
    paginate_by = 9
    context_object_name = 'items'   # your own name for the list as a template variable
    template_name = 'home.html'  # Specify your own template name/location

    def get_queryset(self):
        if not self.request.user.is_customer:
            return redirect('dashboard')
    
        queryset = super(homeView, self).get_queryset().order_by('name')
        return queryset
       
@login_required
def productView(request,pk):
    product = Product.objects.get(pk=pk)
    has_purchased = Order.objects.filter(customer=request.user.customer,product=product)
    reviews = product.review_set.all()
    return render(request,'customer/product_display.html',{'product':product,'reviews':reviews,'has_purchased':has_purchased})

@login_required
def showCartItemView(request,is_wished):
    if request.user.is_customer:
        cart_items = CartItem.objects.filter(customer=request.user.customer,is_wished=is_wished)
        return render(request,'customer/list_cart.html',{'cart_items':cart_items,"is_wished":int(is_wished)})
    else:
        raise PermissionDenied

@login_required
def removeCartItem(request,pk):
    cart_item = CartItem.objects.get(pk=pk)
    is_wished = cart_item.is_wished
    if cart_item.customer == request.user.customer:
        cart_item.delete()
        return redirect(reverse('show_cart_items', kwargs={"is_wished": int(is_wished)}))
    else:
        raise PermissionDenied
    

@login_required
def addToCartView(request,pk,is_wished):
    if request.user.is_customer and request.method == 'POST':
        q = request.POST['quantity']
        cart_item = CartItem(customer=request.user.customer,product=Product.objects.get(pk=pk),quantity=q,is_wished=is_wished)
        cart_item.save()
        # TODO
        return redirect('home')
        
    else :
        raise PermissionDenied
    
@login_required
def buyProductView(request,pk):
    if request.method=='POST' and request.user.is_customer:
        c = request.user.customer
        quantity = int(request.POST['quantity'])
        product=Product.objects.get(pk=pk)
        if 'success' == product.place_order(request,c,quantity):
            return redirect('home')
        else :
            print("something went Wrong")

@login_required
def buyMultiItemView(request):
    if request.user.is_customer:
        cart_items = request.user.customer.cartitem_set.filter(is_wished=0)
        cost = sum([i.product.price * i.quantity for i in cart_items])
        in_stock = all([i.product.quantity >= i.quantity for i in cart_items ])
        if request.user.customer.wallet_balance >= cost and in_stock:
            for i in cart_items:
                c = request.user.customer
                if i.product.place_order(request,c,i.quantity) == 'success':
                    i.delete()
        return redirect('home')            

@login_required
def orderDetailView(request,pk):
    order = Order.objects.get(pk=pk)
    return render(request,'customer/order_detail.html',{'order':order})

@login_required
def customerOrdersView(request):
    if request.user.is_customer:
        orders = Order.objects.filter(customer=request.user.customer)
        print(orders)
        return render(request,'customer/list_orders.html',{'orders':orders})
    else: 
        raise PermissionDenied

@login_required
def addReview(request,pk):
    if request.user.is_customer:
        review_text = request.POST["review"]
        review = Review(product=Product.objects.get(pk=pk),customer=request.user.customer,customer_review=review_text)
        review.save()
        return redirect(reverse('product_display', kwargs={"pk": pk}))
    else: 
        raise PermissionDenied


class addBalanceView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'customer/add_balance.html',{})
    
    def post(self,request):
        amount = int(request.POST['amount'])
        if amount > 0 and request.user.is_customer:
            c = request.user.customer
            c.wallet_balance += amount
            c.save() 
            return redirect('home')
        else: 
            #TODO implement error message 
            print('please enter a valid value')

class customerRegisterView(View):
    def get(self, request):
        user_form = CustomUserCreationForm()
        profile_form = CustomerForm()
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'users/register.html', context)
    
    def post(self,request):
        user_form = CustomUserCreationForm(
            request.POST 
        )
        profile_form = CustomerForm(
            request.POST
        )

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_customer = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.cuser = user
            profile.save()

            return redirect('dashboard')

        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            return render(request, 'users/register.html', context)

class sellerRegisterView(View):
    def get(self, request):
        user_form = CustomUserCreationForm()
        profile_form = SellerForm()
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'users/register.html', context)
    
    def post(self,request):
        user_form = CustomUserCreationForm(
            request.POST 
        )
        profile_form = SellerForm(
            request.POST
        )

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_seller = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.cuser = user
            profile.save()
            return redirect('dashboard')


        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            return render(request, 'users/register.html', context)

