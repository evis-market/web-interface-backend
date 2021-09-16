from django.urls import path

from shop.views import ProductDetailView, RelatedProductsListView, ProductCategoriesListView, ProductsListView


urlpatterns = [
    path('categories/', ProductCategoriesListView.as_view(), name='CategoriesNotEmpty'),
    path('products/', ProductsListView.as_view(), name='Products'),
    path('product/<int:seller_product_id>/', ProductDetailView.as_view(), name='ProductDetail'),
    path('related_products/<int:seller_product_id>/', RelatedProductsListView.as_view(), name='RelatedProducts'),
]
