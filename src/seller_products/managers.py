from django.db import models


class SellerProductBaseManager(models.Manager):

    def get_products_by_seller_id(self, seller):
        return self.model.objects.filter(seller=seller)

    def get_product_by_seller_id(self, pk):
        return self.model.objects.get(pk=pk)


class SellerProductDataSampleManager(models.Manager):
    pass
