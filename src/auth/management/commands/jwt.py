import json
from django.core.management.base import BaseCommand, CommandError

from app import exceptions
from auth.service import JWTAuthService
from users.managers import UserManager
from users.models import User


class Command(BaseCommand):
    help = 'Get user token'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            'grant',
            nargs='+',
            type=str,
            help='Find user by email/phone/erc20',
        )

    def handle(self, *args, **options):
        if options['grant']:
            try:
                user = UserManager.get_by_login(options['grant'][1])
            except exceptions.NotFound:
                raise CommandError('User does not exist')
            self.stdout.write(json.dumps(JWTAuthService.get_tokens_for_user(user), indent=4))

        self.stdout.write(self.style.SUCCESS('Successfully received a tokens'))
