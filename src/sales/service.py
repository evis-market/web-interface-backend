from app import exceptions

from sales.models import Sale


class SalesService:
    NOTFOUND_SALES_MSG = 'Sales not found'

    def get_buyer_shopping_list(self, buyer_id: int):
        shopping_list = Sale.objects.list_by_buyer_id(buyer_id)
        if not shopping_list:
            raise exceptions.NotFound(msg=self.NOTFOUND_SALES_MSG)
        return shopping_list

    def get_seller_sales_list(self, seller_id: int):
        sales_list = Sale.objects.list_by_buyer_id(seller_id)
        if not sales_list:
            raise exceptions.NotFound(msg=self.NOTFOUND_SALES_MSG)
        return sales_list
