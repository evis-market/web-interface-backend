from django.contrib import admin

from sellers.models import Contact, Seller


class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller_id', 'rating')


admin.site.register(Seller, SellerAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller_id', 'type_id', 'value', 'comment')


admin.site.register(Contact, ContactAdmin)
