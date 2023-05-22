from django.contrib import admin
from .models import Seller, Customer, User, Product, Order
from import_export.admin import ImportExportMixin
from import_export import resources, fields

class OrderResource(resources.ModelResource):
    product = fields.Field(attribute='product__name',
                         column_name='Product')
    username = fields.Field(attribute='customer__cuser__username',
                             column_name='Customer Username')

    class Meta:
        model = Order
        fields = ('order_date', 'order_time','cost','quantity')
        export_order = fields

class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderResource


admin.site.register(Order, OrderAdmin)
# Register your models here.
models = [Seller,Customer,User,Product]
admin.site.register(models)
