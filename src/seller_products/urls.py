from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from seller_products.views import SellerProductsListView, SellerProductsView


urlpatterns = [
    path('my/', SellerProductsListView.as_view(), name='SellerProductsView'),
    path('my/<int:pk>', SellerProductsView.as_view(), name='SellerProductsView'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
