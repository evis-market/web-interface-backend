from app import exceptions
from sales.models import Sale
from sellers.models import Seller


class SalesService:
    FORBIDDEN_SELLER_ACCESS_MSG = 'The current user is not registered as a Seller'

    def get_buyer_shopping_list(self, buyer_id: int):
        return Sale.objects.filter_by_buyer_id(buyer_id).prefetch_related('sale_product')

    def get_seller_sales_list(self, seller_id: int):
        seller = Seller.objects.get_seller_by_user_id(seller_id)
        if not seller:
            raise exceptions.NotFound(msg=self.FORBIDDEN_SELLER_ACCESS_MSG)

        return Sale.objects.filter_by_seller_id(seller_id)
