from django.urls import path

from categories.views import CategoryListView


urlpatterns = [
    path('', CategoryListView.as_view(), name='CategoriesList')
]
