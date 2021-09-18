from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from app import exceptions
from users import models


class UserManager(BaseUserManager):

    def _create_user(self, email=None, phone=None, wallet_erc20=None, password=None, **extra_fields):
        """
        Create and save a user with the given email or phone, or wallet_erc20, and password.
        """
        if not email and not phone and not wallet_erc20:
            raise exceptions.BadRequest('The email or phone, or wallet_erc20 must be set')

        if email:
            email = self.normalize_email(email)

        user = models.User(email=email, phone=phone, wallet_erc20=wallet_erc20, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone=None, wallet_erc20=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, phone=phone, wallet_erc20=wallet_erc20, password=password, **extra_fields)

    def create_superuser(self, email=None, phone=None, wallet_erc20=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise exceptions.BadRequest('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise exceptions.BadRequest('Superuser must have is_superuser=True.')

        return self._create_user(email=email, phone=phone, wallet_erc20=wallet_erc20, password=password, **extra_fields)

    @staticmethod
    def is_exists(email=None, phone=None, wallet_erc20=None):
        if not email and not phone and not wallet_erc20:
            raise exceptions.BadRequest('One of email, phone, wallet_erc20 should be set')

        conds = Q()
        if email:
            conds.add(Q(email=email), Q.OR)
        if phone:
            conds.add(Q(phone=phone), Q.OR)
        if wallet_erc20:
            conds.add(Q(wallet_erc20=wallet_erc20), Q.OR)

        if models.User.objects.filter(conds).first():
            return True

        return False

    @staticmethod
    def get_by_email(email):
        try:
            return models.User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise exceptions.NotFound('User not found')

    @staticmethod
    def get_by_login(login):
        try:
            if login.count('@'):
                user = models.User.objects.get(email=login)
            else:
                user = models.User.objects.get(phone=login)
        except ObjectDoesNotExist:
            raise exceptions.NotFound('User not found')

        return user

    def update_secret_code(self, user, secret_code=''):
        user.secret_code = secret_code
        user.save(update_fields=['secret_code'])
