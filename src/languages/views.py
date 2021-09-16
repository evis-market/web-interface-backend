from rest_framework.views import APIView
from app.response import response_ok

from languages.models import Language
from languages.serializers import LanguageSerializer


class LanguagesListView(APIView):
    def get(self):
        langs = Language.objects.all()
        serializer = LanguageSerializer(langs, many=True)
        return response_ok({'langs': serializer.data})
