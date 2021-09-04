from django.urls import path

from sellers.views import SellerSettingsView


urlpatterns = [
    path('settings/my', SellerSettingsView.as_view(), name='SellerSettingsView'),
]
