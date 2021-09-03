from sellers import models


class SellerManager:

    @staticmethod
    def get_seller_by_user_id(user_id):
        return models.Seller.objects.filter(seller_id=user_id).first()

    @staticmethod
    def get_seller_contacts_by_seller_id(seller_id):
        return models.Contact.objects.filter(seller_id=seller_id)

    @staticmethod
    def delete_seller_contacts_by_seller_id(seller_id):
        return models.Contact.objects.filter(seller_id=seller_id).delete()
