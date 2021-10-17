from sales.models import Sale


class SalesService:

    def get_buyer_shopping_list(self, buyer_id: int):
        return Sale.objects.filter_by_buyer_id(buyer_id)

    def get_seller_sales_list(self, seller_id: int):
        return Sale.objects.filter_by_buyer_id(seller_id)
