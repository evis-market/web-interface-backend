from rest_framework.views import APIView

from app.response import response_ok
from languages.models import Language
from languages.serializers import LanguageSerializer


class LanguagesListView(APIView):
    """
    URL: `/api/v1/langs/`

    Method: `GET`

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",

          "langs": [
            {
              "id": 1,
              "name_native": "English",
              "name_en": "English",
              "slug": "en"
            },
            {
              "id": 2,
              "name_native": "Русский",
              "name_en": "Russian",
              "slug": "ru"
            }
          ]
        }
    """
    def get(self):
        langs = Language.objects.all()
        serializer = LanguageSerializer(langs, many=True)
        return response_ok({'langs': serializer.data})
