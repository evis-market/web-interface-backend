from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager

from users import models


class UserManager(UserManager):

    def _create_user(self, email=None, phone=None, wallet_erc20=None, password=None, **extra_fields):
        """
        Create and save a user with the given email or phone, or wallet_erc20, and password.
        """
        if not email and not phone and not wallet_erc20:
            raise ValueError('The email or phone, or wallet_erc20 must be set')

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
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email=email, phone=phone, wallet_erc20=wallet_erc20, password=password, **extra_fields)
