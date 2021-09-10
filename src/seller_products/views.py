from rest_framework.exceptions import APIException, NotFound
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.views import APIView

from app.response import response_ok, response_err
from seller_products.models import SellerProduct
from seller_products.serializers import SellerProductsSerializer
from seller_products.filters import SellerProductFilter
from sellers.models import Seller


class SellerProductsListView(GenericAPIView):
    """

    """
    serializer_class = SellerProductsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')

        if user_id and not Seller.objects.get_seller_by_user_id(user_id):
            raise APIException(f'User with id = {user_id} is not registered as a Seller', 400)

        queryset = SellerProduct.objects.all()
        seller_product_filter = SellerProductFilter(request.GET.copy(), queryset=queryset)
        serializer = self.serializer_class(seller_product_filter.qs, many=True)
        return response_ok({'seller-products': serializer.data})

    def post(self, request, format=None):
        seller = Seller.objects.get(seller_id=request.user.id)

        if not seller:
            raise APIException('The current user is not registered as seller', 400)

        request.data['seller_id'] = seller.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return response_ok(serializer.data)


class SellerProductsView(APIView):
    """

    """
    serializer_class = SellerProductsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return SellerProduct.objects.get_product_by_seller_id(pk=pk)
        except SellerProduct.DoesNotExist:
            raise NotFound(f'Seller_product with id = {pk} not found')

    def get(self, request, pk, format=None):
        seller_product = self.get_object(pk)
        serializer = self.serializer_class(seller_product)
        return response_ok(serializer.data)

    def put(self, request, pk, format=None):
        seller_product = self.get_object(pk)
        serializer = self.serializer_class(seller_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_ok(serializer.data)
        return response_err(400, 'bad', 400)

    def delete(self, request, pk, format=None):
        pass
