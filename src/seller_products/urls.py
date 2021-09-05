from django.urls import path

from seller_products.views import SellerProductsListView, SellerProductsView


urlpatterns = [
    path('', SellerProductsListView.as_view(), name='SellerProductsView'),
    path('<int:pk>/', SellerProductsView.as_view(), name='SellerProductsView'),

]
