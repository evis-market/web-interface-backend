from django.contrib import admin

from sales.models import Sale


class SalesAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'uuid', 'seller', 'buyer', 'amount')
    search_fields = ('seller', 'buyer', 'amount')


admin.site.register(Sale, SalesAdmin)
