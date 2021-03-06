from django.urls import path

from sales.views import SalesBuyerShoppingListView, SellerSalesListView


urlpatterns = [
    path('buyer_shopping_list', SalesBuyerShoppingListView.as_view(), name='BuyerShoppingList'),
    path('seller_sales_list', SellerSalesListView.as_view(), name='SellerSalesList'),
]
