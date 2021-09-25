from django.core.mail import send_mail
from django.template.loader import render_to_string

from users.models import User


class UsersService:
    def __init__(self, domain: str):
        self.domain = domain

    def signup(self, data: dict):
        for p in ('phone', 'email', 'wallet_erc20'):
            if not data[p]:
                del data[p]

        user = User.objects.create_user(**data)

        if data['email']:
            self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user: User):
        User.objects.update_secret_code(user, user.gen_secret_code())
        message = render_to_string('confirm_email.txt', {
            'user': user,
            'domain': self.domain,
        })
        send_mail('Confirm your email', message, None, [user.email])

    def update_user_profile(self, user: User, data: dict) -> None:
        User.objects.update(
            user=user,
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone': data['phone'],
                'email': data['email'],
                'wallet_for_payments_erc20': data['wallet_for_payments_erc20'],
            })
