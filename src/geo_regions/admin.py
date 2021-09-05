from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from mptt.admin import MPTTModelAdmin

from geo_regions.models import GeoRegion


class GeoRegionAdmin(MPTTModelAdmin):
    list_display = ('name', 'iso_code', 'parent')
    list_filter = (
        ('parent', RelatedDropdownFilter),
    )
    search_fields = ('name', 'iso_code')


admin.site.register(GeoRegion, GeoRegionAdmin)
