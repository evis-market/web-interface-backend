from django.urls import path

from geo_regions.views import GeoRegionListView


urlpatterns = [
    path('', GeoRegionListView.as_view(), name='GeoRegionsList'),
]
