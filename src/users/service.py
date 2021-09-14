from app import exceptions
from users.models import User


class UsersService:
    def signup(self, data: dict):
        user = User.objects.create_user(**data)

        if data['email']:
            # TODO: send confirmation email
            pass

        return user
