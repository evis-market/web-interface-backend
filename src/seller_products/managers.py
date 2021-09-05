from django.db import models


class SellerProductManager(models.Manager):

    def get_products_by_user_id(self, seller):
        return self.model.objects.filter(seller=seller)