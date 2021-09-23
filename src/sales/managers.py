from django.db import models


class SaleManager(models.Manager):

    def list_by_seller_id(self, seller):
        return self.model.objects.select_related('seller').filter(seller=seller)

    def list_by_buyer_id(self, buyer):
        return self.model.objects.select_related('users').filter(user=buyer)


class SaleProductManager(models.Manager):
    pass
