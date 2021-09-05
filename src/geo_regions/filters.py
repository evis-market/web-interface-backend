from django_filters import rest_framework as filters

from geo_regions.models import GeoRegion


class GeoRegionFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    parent_id = filters.CharFilter(method='parent_id_filter')

    class Meta:
        model = GeoRegion
        fields = []

    def parent_id_filter(self, queryset, name, value):
        try:
            int_val = int(value)
        except ValueError:
            int_val = 0

        if value == 'null' or int_val < 1:
            return queryset.filter(parent_id__isnull=True)

        return queryset.filter(parent_id=int_val)
