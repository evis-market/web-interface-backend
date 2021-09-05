from django.contrib import admin

from product_data_types.models import DataFormat, DataType


class DataFormatInline(admin.TabularInline):
    model = DataFormat


class DataTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    inlines = [
        DataFormatInline,
    ]


class DataFormatAdmin(admin.ModelAdmin):
    list_display = ('name', 'data_type_id', 'id')
    search_fields = ('name',)


admin.site.register(DataType, DataTypeAdmin)
admin.site.register(DataFormat, DataFormatAdmin)
