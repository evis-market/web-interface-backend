from django.urls import path

from reference.views import GeoRegionListView


urlpatterns = [
    path('geo-regions/', GeoRegionListView.as_view(), name='GeoRegionsList')
]
