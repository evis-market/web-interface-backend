import pytz
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)

    first_name = models.CharField('First name', max_length=150, blank=True)
    last_name = models.CharField('Last name', max_length=150, blank=True)
    email = models.EmailField('Email', max_length=190, blank=True, null=True, unique=True)
    is_email_confirmed = models.BooleanField('Email confirmed', blank=True, default=False)
    phone = models.CharField('Phone', blank=True, null=True, unique=True, max_length=15)
    is_phone_confirmed = models.BooleanField('Phone confirmed', blank=True, default=False)
    wallet_erc20 = models.CharField('ERC-20 wallet', blank=True, null=True, unique=True, max_length=42)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    is_staff = models.BooleanField(
        'Staff status',
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        'Is active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    secret_code = models.CharField('Secret code', max_length=8, blank=True, default='')
    timezone = models.CharField(choices=tuple(zip(pytz.all_timezones, pytz.all_timezones)),
                                max_length=32, default='UTC')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('last_name', 'first_name')

    def username(self):
        return self.email or self.phone or self.wallet_erc20

    @classmethod
    def parse_name(cls, name: str) -> dict:
        if name is None:
            return {}

        parts = name.split(' ', 2)

        if len(parts) == 1:
            return {'first_name': parts[0]}

        if len(parts) == 2:
            return {'first_name': parts[0], 'last_name': parts[1]}

        return {'first_name': parts[0], 'last_name': ' '.join(parts[1:])}

    def __str__(self):
        name = self.first_name + ' ' + self.last_name

        if len(name) < 3:
            return self.username()

        return name.strip()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @staticmethod
    def gen_secret_code():
        return UserManager.make_random_password(length=8)
