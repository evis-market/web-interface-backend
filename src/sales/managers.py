from django.db import models


class SaleManager(models.Manager):

    def filter_by_seller_id(self, seller):
        return self.model.objects.filter(seller=seller)

    def filter_by_buyer_id(self, buyer):
        return self.model.objects.filter(buyer=buyer)


class SaleProductManager(models.Manager):
    pass
