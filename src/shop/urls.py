from django.urls import path

from shop.views import ProductDetailView, RelatedProductsListView


urlpatterns = [
    path('product/<int:seller_product_id>/', ProductDetailView.as_view(), name='Shop'),
    path('related_products/<int:seller_product_id>/', RelatedProductsListView.as_view(), name='Shop'),
]
