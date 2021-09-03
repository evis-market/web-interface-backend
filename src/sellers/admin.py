from django.contrib import admin

from sellers.models import Contact, Seller


class ContactInline(admin.TabularInline):
    model = Contact


class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller_id', 'rating')
    inlines = [
        ContactInline,
    ]

admin.site.register(Seller, SellerAdmin)
