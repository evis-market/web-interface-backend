import json
from importlib import import_module

import pytest
from django.conf.global_settings import SESSION_ENGINE
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from auth.views import GrantJWTTokenView
from users.models import User

pytestmark = pytest.mark.django_db


class TestCustomLoginView:

    def test_post_with_email(self):
        """
        Test: login by user with email
        """
        user = mixer.blend(User,
                           email="newuser@gmail.com",
                           phone=None,
                           password="test_password_1")
        user.set_password("test_password_1")
        user.save()
        data = {
            "grant_type": "password",
            "login": user.email,
            "password": "test_password_1"
        }
        url = reverse("GrantJWTTokenView")
        request = APIRequestFactory().post(url, data=json.dumps(data), content_type="application/json")
        # this is needed for the login(request, user, backend) function
        request.session = import_module(SESSION_ENGINE).SessionStore(None)
        response = GrantJWTTokenView.as_view()(request=request)
        assert response.status_code == 200
