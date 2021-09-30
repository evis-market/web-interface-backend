from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import signing
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.models import User

from app import exceptions

NOTFOUND_USER_MSG = 'User not found'
INVALID_SECRET_CODE_MSG = 'invalid secret code'


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            signing.dumps(obj=getattr(user, user.USERNAME_FIELD))
        )


account_activation_token = TokenGenerator()


class SignupService:
    def __init__(self, domain: str):
        self.domain = domain

    def signup(self, data: dict):
        for p in ('phone', 'email', 'wallet_erc20'):
            if p in data and not data[p]:
                del data[p]

        user = User.objects.create_user(**data)

        if 'email' in data and data['email']:
            self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user: User):
        User.objects.update_secret_code(user, user.gen_secret_code())
        message = render_to_string('confirm_email.txt', {
            'user': user,
            'domain': self.domain,
        })
        send_mail('Confirm your email', message, None, [user.email])

    def confirm_email(self, data: dict):
        user = User.objects.get_by_login(data['email'])
        if not user:
            raise exceptions.NotFound(msg=NOTFOUND_USER_MSG)
        if not account_activation_token.check_token(user, data['secret_code']):
            raise exceptions.NotFound(msg=INVALID_SECRET_CODE_MSG)
        user.is_active = True
        user.save()

    def send_reset_password_email(self, data: dict, domain):
        if 'email' not in data or not data['email']:
            raise exceptions.NotFound(msg='email not found')
        user = User.objects.get_by_login(data['email'])
        if not user:
            raise exceptions.NotFound('User not found')
        message = render_to_string('activate_account.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'secret_code': account_activation_token.make_token(user),
        })
        to_email = data['email']
        email = EmailMessage('Reset your password', message, to=[to_email])
        email.send()


class UsersService:
    def update_profile(self, user: User, data: dict) -> None:
        User.objects.update(
            user=user,
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone': data['phone'],
                'email': data['email'],
                'wallet_for_payments_erc20': data['wallet_for_payments_erc20'],
            })

    def update_password(self, user: User, data: dict) -> None:
        User.objects.update(
            user=user,
            defaults={
                'password': data['password'],
            })
