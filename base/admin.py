from django.contrib import admin
from . models import ProductModel,CartModel, OrderModel
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    model = ProductModel
    list_display = ['pname','price','pcategory','pimage']
admin.site.register(ProductModel,ProductAdmin)
admin.site.register(CartModel)
admin.site.register(OrderModel)