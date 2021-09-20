from app import exceptions
from seller_products.models import SellerProduct


class ShopService:

    def get_shop_products(self, category_ids, order_by_fields, order_by_allowed_fields):
        shop_products = SellerProduct.objects.get_seller_products_by_categories(category_ids)
        return self.order_by_queryset(shop_products, order_by_fields, order_by_allowed_fields)

    def order_by_queryset(self, queryset, order_by_fields, order_by_allowed_fields):
        if not set(order_by_fields).issubset(order_by_allowed_fields):
            raise exceptions.NotFound('One or more fields are set in order by conditions are not allowed'
                                      f'Allowed fields = {"".join(order_by_allowed_fields)}'
                                      f'Set fields = {"".join(order_by_fields)}')

        return queryset.order_by(*order_by_fields)