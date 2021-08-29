from django_filters import rest_framework as filters

from categories.models import Category


class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    parent_id = filters.CharFilter(method='parent_id_filter')

    class Meta:
        model = Category
        fields = []

    def parent_id_filter(self, queryset, name, value):
        int_val = int(value)
        if value == 'null' or int_val == 0:
            return queryset.filter(parent_id__isnull=True)

        if int_val > 0:
            return queryset.filter(parent_id__eq=int_val)

        return queryset
