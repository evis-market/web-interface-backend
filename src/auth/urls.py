from django.urls import path

from auth.views import GrantJWTTokenView

urlpatterns = [
    path('jwt/grant', GrantJWTTokenView.as_view(), name='GrantJWTTokenView'),
]
