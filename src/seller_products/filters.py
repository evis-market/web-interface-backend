from django_filters import rest_framework as filters

from seller_products.models import SellerProduct


class SellerProductFilter(filters.FilterSet):
    seller = filters.NumberFilter()

    class Meta:
        model = SellerProduct
        fields = []
