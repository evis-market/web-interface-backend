from django.contrib import admin

from seller_products.models import SellerProduct
# Register your models here.


class SellerProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'descr')


admin.site.register(SellerProduct, SellerProductAdmin)
