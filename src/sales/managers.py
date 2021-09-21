from django.db import models


class SaleManager(models.Manager):

    def list_by_seller_id(self, seller_id):
        return self.model.objects.filter(seller_user_id=seller_id)

    def list_by_buyer_id(self, buyer_id):
        return self.model.objects.filter(buyer_user_id=buyer_id)


class SaleProductManager(models.Manager):
    pass
