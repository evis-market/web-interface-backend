from django.core.management.base import BaseCommand, CommandError

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
            except User.DoesNotExist:
                raise CommandError(f'User does not exist')
            print(JWTAuthService.get_tokens_for_user(user))

        self.stdout.write(self.style.SUCCESS('Successfully received a tokens'))
