from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import signing
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.db.models import Q

from app import exceptions
from users.models import User

INVALID_SECRET_CODE_MSG = 'invalid secret code'


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            signing.dumps(obj=getattr(user, user.USERNAME_FIELD))
        )


account_activation_token = TokenGenerator()


class SignupService:
    SECRET_CODE_LENGTH = 8

    def __init__(self, domain: str):
        self.domain = domain

    def signup(self, data: dict):
        user = User.objects.create_user(**data)

        if 'email' in data and data['email']:
            self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user: User):
        User.objects.update_secret_code(user, User.objects.gen_secret_code())
        message = render_to_string('confirm_email.txt', {
            'user': user,
            'domain': self.domain,
        })
        send_mail('Confirm your email', message, None, [user.email])

    def confirm_email(self, data: dict):
        user = User.objects.get_by_login(data['email'])
        if not account_activation_token.check_token(user, data['secret_code']):
            raise exceptions.BadRequest(msg=INVALID_SECRET_CODE_MSG)
        user.is_email_confirmed = True
        user.save()

    def set_password_by_secret_code(self, data: dict):
        if 'email' not in data or not data['email']:
            raise exceptions.NotFound(msg='email not found')
        user = User.objects.get_by_login(data['email'])
        if not account_activation_token.check_token(user, data['secret_code']):
            raise exceptions.BadRequest(msg=INVALID_SECRET_CODE_MSG)
        user.set_password(data['password'])
        user.save()

    def send_reset_password_email(self, data: dict, domain):
        if 'email' not in data or not data['email']:
            raise exceptions.NotFound(msg='email not found')
        user = User.objects.get_by_login(data['email'])
        message = render_to_string('activate_account.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'secret_code': account_activation_token.make_token(user),
        })
        email = EmailMessage('Reset your password', message, to=[data['email']])
        email.send()


class UsersService:
    def update_profile(self, user: User, data: dict) -> None:
        if User.objects.filter(~Q(uuid=user.uuid), Q(email=data['email'])).first():
            raise exceptions.BadRequest('Email has been already taken by someone else')

        if User.objects.filter(~Q(uuid=user.uuid), Q(email=data['phone'])).first():
            raise exceptions.BadRequest('Phone has been already taken by someone else')

        if User.objects.filter(~Q(uuid=user.uuid), Q(email=data['wallet_erc20'])).first():
            raise exceptions.BadRequest('Wallet_erc20 has been already taken by someone else')

        User.objects.filter(uuid=user.uuid).update(**data)

    def update_user_password(self, user: User, password: str) -> None:
        user.set_password(password)
        user.save()
