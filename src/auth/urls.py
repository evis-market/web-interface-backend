from django.urls import path

from auth.views import CustomLoginView

urlpatterns = [
    path('jwt/grant/', CustomLoginView.as_view()),
]
