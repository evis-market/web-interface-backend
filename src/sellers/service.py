from sellers.managers import SellerManager
from sellers.models import Contact, Seller
from users.models import User


class SellerService:

    def create_seller(self,
                      user: User,
                      data: dict) -> None:
        seller, created = Seller.objects.update_or_create(
            seller_id=user,
            defaults={'name': data['name'],
                      'description': data['description'],
                      'logo_url': data['logo_url'],
                      'wallet_for_payments_erc20': data['wallet_for_payments_erc20']})
        self.save_contacts(contacts=data['contacts'],
                           seller=seller if created else SellerManager.get_seller_by_user_id(user.id))

    @staticmethod
    def save_contacts(contacts: list,
                      seller: Seller) -> None:
        SellerManager.delete_seller_contacts_by_seller_id(seller.id)
        for contact in contacts:
            Contact(seller_id=seller,
                    type_id=contact['type_id'],
                    value=contact['value'],
                    comment=contact['comment']).save()
