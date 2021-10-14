from django_filters import rest_framework as filters

from categories.models import Category


class CategoryFilter(filters.FilterSet):
    """ Class representing category filter

    Attributes:
        name (django_filters.filters): filter field
        parent_id (django_filters.filters):filter field
    """
    name = filters.CharFilter(lookup_expr='icontains')
    parent_id = filters.CharFilter(method='parent_id_filter')

    class Meta:
        model = Category
        fields = []

    def parent_id_filter(self, queryset, name, value):
        """ Filter by parent_id.

        Args:
            queryset: filter query set
            name: name value for filter
            value: filter value

        Returns:
            Filter by parent_id.
        """
        try:
            int_val = int(value)
        except ValueError:
            int_val = 0

        if value == 'null' or int_val < 1:
            return queryset.filter(parent_id__isnull=True)

        return queryset.filter(parent_id=int_val)
