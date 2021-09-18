from django.db import models


class SellerManager(models.Manager):

    def get_seller_by_user_id(self, user_id):
        return self.model.objects.filter(seller_id=user_id).first()


class ContactManager(models.Manager):

    def get_seller_contacts_by_seller_id(self, seller_id):
        return self.model.objects.filter(seller_id=seller_id)

    def delete_seller_contacts_by_seller_id(self, seller_id):
        return self.model.objects.filter(seller_id=seller_id).delete()
