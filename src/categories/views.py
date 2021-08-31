from rest_framework.views import APIView

from app.response import response_ok
from categories.filters import CategoryFilter
from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryListView(APIView):
    """
    URL: `/api/v1/categories/`

    Method: `GET`

    **URL params**

    * parent_id - parent category id
    * name - category name filter

    **Example query**

        /api/v1/categories/?name=data&parent_id=1


    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",

          "categories": [
            {
              "id": 1,
              "parent_id": null,
              "name": "Category1 name",
              "descr": "Category1 description",
              "logo_url": "https://domain.com/logo1.jpg",
              "slug": "category1",
              "sort_id": 1,
              "recommended_for": [
                "For Traiders",
                "For Analytics",
                "For Personal Use"
              ]
            },
            {
              "id": 2,
              "parent_id": null,
              "name": "Category2 name",
              "descr": "Category2 description",
              "logo_url": "https://domain.com/logo2.jpg",
              "slug": "category2",
              "sort_id": 90,
              "recommended_for": [
                "For Scientists",
                "For Personal Use"
              ]
            }
          ]
        }

    **Empty or not found response**

        HTTP status Code: 200

        {
          "status": "OK",
          "categories": []
        }
    """
    def get(self, request, format=None):
        queryset = Category.objects.all()
        categories_filter = CategoryFilter(request.GET.copy(), queryset=queryset)
        serializer = CategorySerializer(categories_filter.qs, many=True)
        return response_ok({'categories': serializer.data})
