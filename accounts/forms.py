from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer,Seller,User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name','password1','password2')

# create a ModelForm
class CustomerForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = Customer
		fields = "__all__"
		exclude = ['cuser']

# create a ModelForm
class SellerForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = Seller
		fields = "__all__"
		exclude = ['cuser']

