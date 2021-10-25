from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from app.response import response_ok
from sales.selializers import SellerSalesListSerializer, ShoppingListSerializer
from sales.service import SalesService


class SalesBuyerShoppingListView(GenericAPIView):
    """
    ## Get buyer shopping list

    URL: `/api/v1/sales/buyer_shopping_list`

    Method: `GET`

    **Successful response**

        {
          "status": "OK",

          "sales": [
            {
              ...
            },
            {
              ...
            }
          ]
        }
    """
    serializer_class = ShoppingListSerializer

    def get(self, request):
        sales_service = SalesService()
        buyer_shopping_list = sales_service.get_buyer_shopping_list(buyer_id=request.user.id)
        serializer = self.serializer_class(buyer_shopping_list, many=True)
        return response_ok({'shopping_list': serializer.data})


class SellerSalesListView(GenericAPIView):
    """
    ## Get seller sold products

    URL: `/api/v1/sales/seller_sales_list`

    Method: `GET`

    **Successful response**

        {
          "status": "OK",
          "sales": [
            {
              ...
            },
            {
              ...
            }
          ]
        }
    """
    serializer_class = SellerSalesListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sales_service = SalesService()
        seller_sales_list = sales_service.get_seller_sales_list(seller_id=request.user.id)
        serializer = self.serializer_class(seller_sales_list, many=True)
        return response_ok({'sales': serializer.data})
