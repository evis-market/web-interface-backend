from sellers.models import Seller
from rest_framework.exceptions import APIException


class SellerProductMixin:

    def get_seller(self, request):
        seller = Seller.objects.filter(seller=request.user.id).first()

        if not seller:
            raise APIException('The current user is not registered as a Seller', 403)

        return seller
