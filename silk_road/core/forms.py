
# create a ModelForm
from django import forms

from silk_road.core.models import Product


class ProductForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = Product
		fields = "__all__"
		exclude = ['seller']
