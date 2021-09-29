from rest_framework.generics import GenericAPIView

from app.response import response_ok
from sales.service import SalesService

from sales.selializers import SalesSerializer


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
    serializer_class = SalesSerializer

    def get(self, request):
        sales_service = SalesService()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        buyer_shopping_list = sales_service.get_buyer_shopping_list(buyer_id=request.user.id)
        return response_ok({'sales': buyer_shopping_list})


class SellerSalesListView(GenericAPIView):
    """
    ## Get seller sales list

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
    serializer_class = SalesSerializer

    def get(self, request):
        sales_service = SalesService()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        seller_sales_list = sales_service.get_seller_sales_list(seller_id=request.user.id)
        return response_ok({'sales': seller_sales_list})
