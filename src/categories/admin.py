from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from mptt.admin import MPTTModelAdmin

from categories.models import Category


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = (
        ('parent', RelatedDropdownFilter),
    )
    search_fields = ('name', 'slug')


admin.site.register(Category, CategoryAdmin)
