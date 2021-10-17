from django.db import models


class SellerManager(models.Manager):

    def get_seller_by_user_id(self, user_id):
        return self.model.objects.filter(seller_id=user_id).first()


class ContactManager(models.Manager):

    def get_all_by_seller(self, seller_id):
        return self.model.objects.filter(seller_id=seller_id)

    def delete_all_by_seller(self, seller_id):
        return self.model.objects.filter(seller_id=seller_id).delete()
