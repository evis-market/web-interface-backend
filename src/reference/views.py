from rest_framework.views import APIView

from app.response import response_ok
from reference.filters import GeoRegionFilter
from reference.models import GeoRegion
from reference.serializers import GeoRegionSerializer


class GeoRegionListView(APIView):
    """
    URL: `/api/v1/reference/geo_region/`

    Method: `GET`

    **URL params**

    * parent_id - parent geo-region id
    * name - geo-region name filter

    **Example query**

        /api/v1/reference/geo_region/?name=Brazil&parent_id=1


    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",

          "geo_regions": [
            {
                "id": 1,
                "name": "Europe",
                "parent_id": null,
                "iso_code": "EU"
            },
            {
                "id": 1,
                "name": "Spain",
                "parent_id": 1,
                "iso_code": "EU"
            },
          ]
        }

    **Empty or not found response**

        HTTP status Code: 200

        {
            "geo_regions": [],
            "status": "OK"
        }
    """
    def get(self, request, format=None):
        queryset = GeoRegion.objects.all()
        categories_filter = GeoRegionFilter(request.GET.copy(), queryset=queryset)
        serializer = GeoRegionSerializer(categories_filter.qs, many=True)
        return response_ok({'geo_regions': serializer.data})
