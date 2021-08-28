import uuid

import pytest
from mixer.backend.django import mixer
from users.models import User

mixer.register(User,
               uuid=lambda: uuid.uuid4())


@pytest.fixture
def superuser():
    return mixer.blend(User,
                       username='superuser@gmail.com',
                       is_superuser=True)
