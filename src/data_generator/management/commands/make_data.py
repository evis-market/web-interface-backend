import logging
import random
from django.core.management.base import BaseCommand
from django.db import transaction

from categories.models import Category
from data_generator import factories
from seller_products.models import SellerProduct
from sellers.models import Seller
from users.models import User


class Command(BaseCommand):
    help = 'Make test data for apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '-cu',
            '--count_users',
            default=50,
            type=int,
        )

        parser.add_argument(
            '-cp',
            '--count_products',
            default=1000,
            type=int,
        )

        parser.add_argument(
            '-ccp',
            '--count_categories_per_product',
            default=10,
            type=int,
        )

    def handle(self, *args, **options):
        c_users = options['count_users']
        c_product = options['count_products']
        c_categories_per_product = options['count_categories_per_product']
        categories = Category.objects.all()

        with transaction.atomic():
            self._clear_models_data()
            self._create_models_data(categories, c_users, c_product, c_categories_per_product)

    def _create_seller_products(self, categories, c_seller_products, c_categories_per_product):
        SellerProduct.objects.bulk_create(
            SellerProduct(seller=seller) for _ in range(c_seller_products)
            for seller in Seller.objects.all()
        )
        logging.info('SellerProducts created..')

        c_left = SellerProduct.objects.all().count()
        for seller_product in SellerProduct.objects.all():
            category_ids = [
                choice.id for choice in random.choices(categories, k=random.randint(1, c_categories_per_product))
            ]
            seller_product.categories.add(*category_ids)
            c_left -= 1
            logging.info('SellerProducts are left to processed %s..', c_left)

    def _create_sellers(self, user):
        pass

    def _clear_models_data(self):
        Seller.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def _create_models_data(self, categories, c_users, c_seller_products, c_categories_per_product):
        users = [factories.UserFactory() for _ in range(c_users)]
        logging.info('Users created..')

        Seller.objects.bulk_create(
            Seller(seller=user) for user in users
        )
        logging.info('Sellers created..')

        self._create_seller_products(categories, c_seller_products, c_categories_per_product)
