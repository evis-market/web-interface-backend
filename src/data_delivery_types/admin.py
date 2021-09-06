from django.contrib import admin

from data_delivery_types.models import DataDeliveryType


class DataDeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


admin.site.register(DataDeliveryType, DataDeliveryTypeAdmin)
