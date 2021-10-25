from app import exceptions
from seller_products.models import SellerProduct


class ShopService:
    """ Class representing shop service """

    def get_shop_products(self, name, category_ids, order_by_fields, order_by_allowed_fields):
        """ Get shop products.

        Returns:
            Filtered and ordered products.
        """
        shop_products = SellerProduct.objects.get_seller_products_by_categories_and_name(name, category_ids)

        if not set(order_by_fields).issubset(order_by_allowed_fields):
            raise exceptions.NotFound('One or more fields are set in order by conditions are not allowed'
                                      f'Allowed fields = {", ".join(order_by_allowed_fields)}'
                                      f'Set fields = {", ".join(order_by_fields)}')
        return shop_products.order_by(*order_by_fields)

    def get_category_ids(self, request):
        category_ids = []

        for category_id in request.GET.get('category_ids', '').split(','):
            try:
                category_ids.append(int(category_id))
            except ValueError:
                pass
        return category_ids

    def get_order_by(self, request):
        order_by_fields = []
        for field in request.GET.get('order_by', '').split(','):
            if field != '':
                order_by_fields.append(field)
        return order_by_fields
