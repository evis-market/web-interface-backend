from django.urls import path

from languages.views import LanguagesListView


urlpatterns = [
    path('', LanguagesListView.as_view(), name='LanguagesList'),
]
