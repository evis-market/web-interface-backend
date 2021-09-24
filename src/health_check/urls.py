from django.urls import path

from health_check.views import health_check


urlpatterns = [
    path('', health_check, name='healthCheck'),
]
