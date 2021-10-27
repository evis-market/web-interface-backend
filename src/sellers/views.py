from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from app.response import response_ok
from sellers.models import Seller
from sellers.serializer import SellerUpdateSerializer, SellerViewSerializer
from sellers.service import SellerService


class SellerSettingsView(GenericAPIView):
    """
    ## Get seller settings

    Returns seller's data.

    URL: `/api/v1/sellers/settings/my`

    Method: `GET`

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",

          "seller": {
            "id": 1,
            "seller_id": 1,
            "name": "Seller name",
            "description": "Seller description",
            "logo_url": "https://domain.com/logo.jpg",
            "wallet_for_payments_erc20": "0x....",
            "rating": 4.97,
            "contacts": [
              { "id": 1, "type_id": 1, "value": "https://domain1.com/", "comment": "main site" },
              { "id": 2, "type_id": 1, "value": "https://domain2.com/", "comment": "" },
              { "id": 3, "type_id": 2, "value": "1231231231", "comment": "phone1 comment" },
              { "id": 4, "type_id": 2, "value": "1231231232", "comment": "phone2 comment" }
              { "id": 5, "type_id": 3: "value": "email1@test.com", "comment": "email1 comment" },
              { "id": 6, "type_id": 3: "value": "email2@test.com", "comment": "" },
            ]
          }
        }

    **Failed response**

        HTTP status Code: 401

        {
          "status": "ERR",

          "error": {
              "code": 401,
              "msg" : "unauthorized"
          }
        }

    ##  Update seller settings

    Return status OK

     URL: `/api/v1/sellers/settings/my`

    Method: `PUT`

    **Request**

        {
          "status": "OK",

          "seller": {
            "seller_id": 1,
            "name": "Seller name",
            "description": "Seller description",
            "logo_url": "1d5f2241-d55b-43bb-af9f-36d2ce76ab87",
            "wallet_for_payments_erc20": "0x....",
            "contacts": [
              { "id": 1, "type_id": 1, "value": "https://domain1.com/", "comment": "main site" },
              { "id": 3, "type_id": 2, "value": "1231231231", "comment": "phone1 comment" },
              { "id": 5, "type_id": 3, "value": "email1@test.com", "comment": "email1 comment" }
            ]
          }
        }

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK"
        }

    **Failed response**

        HTTP status Code: 400

        {
          "status": "ERR",

          "error": {
              "code": 400,
              "msg" : "bad request",

              "invalid_fields": {
                "name": "to long, 256 symbols maximum",
                "email": "email2#test.com is invalid"
              }
          }
        }
    """
    serializer = SellerViewSerializer
    update_serializer = SellerUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        seller = Seller.objects.get_seller_by_user_id(user_id=request.user.id)
        result = self.serializer(seller).data
        return response_ok({'seller': result})

    def put(self, request):
        seller_service = SellerService()
        serializer = self.update_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            seller_service.create_or_update_object(data=serializer.validated_data, user=request.user)
        return response_ok()
