import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from categories.models import Category
from seller_products.models import SellerProduct
from sellers.models import Seller
from users.models import User


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category


# Defining a factory
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')


class SellerFactory(DjangoModelFactory):
    class Meta:
        model = Seller

    seller = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    wallet_for_payments_erc20 = fuzzy.FuzzyText(length=42)


class SellerProductFactory(DjangoModelFactory):
    class Meta:
        model = SellerProduct

    seller = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    categories = factory.SubFactory(Category)
