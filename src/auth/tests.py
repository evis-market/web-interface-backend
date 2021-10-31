import json
import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from auth.views import GrantJWTTokenView
from users.models import User

pytestmark = pytest.mark.django_db


class TestCustomLoginView:

    def test_post_with_email_and_phone(self):
        """
        Test: login by user with email / phone
        """
        user = mixer.blend(User,
                           email='newuser@gmail.com',
                           phone='12345678',
                           password='test_password_1')
        user.set_password('test_password_1')
        user.save()
        request_data_cases = [
            {
                'grant_type': 'password',
                'login': user.email,
                'password': 'test_password_1',
            },
            {
                'grant_type': 'password',
                'login': user.phone,
                'password': 'test_password_1',
            },
        ]
        url = reverse('GrantJWTTokenView')
        for request_data in request_data_cases:
            request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
            response = GrantJWTTokenView.as_view()(request=request)
            assert response.status_code == 200
            fields = ['refresh_token', 'access_token', 'token_type', 'status']
            assert response.data['token_type'] == 'Bearer'
            assert response.data['status'] == 'OK'
            for field in fields:
                assert field in response.data

    def test_post_with_wallet_erc20(self):
        """
        Test: login by user with wallet ERC-20
        """
        user = mixer.blend(User,
                           wallet_erc20='0xC88E53eda9A20C9aE52e8a222f1a56793188d196',
                           password='test_password_1')
        user.set_password('test_password_1')
        user.save()
        request_data = {
                'grant_type': 'password',
                'login': user.wallet_erc20,
                'password': 'test_password_1',
        }
        url = reverse('GrantJWTTokenView')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = GrantJWTTokenView.as_view()(request=request)
        assert response.status_code == 200
        fields = ['refresh_token', 'access_token', 'token_type', 'status']
        assert response.data['token_type'] == 'Bearer'
        assert response.data['status'] == 'OK'
        for field in fields:
            assert field in response.data

    def test_post_with_refresh_token(self):
        """
        Test: login by user with refresh_token
        """
        user = mixer.blend(User)
        token = RefreshToken.for_user(user)
        request_data = {
            'grant_type': 'refresh_token',
            'refresh_token': str(token),
        }
        url = reverse('GrantJWTTokenView')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = GrantJWTTokenView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['refresh_token'] != token
        fields = ['refresh_token', 'access_token', 'token_type', 'status']
        assert response.data['token_type'] == 'Bearer'
        assert response.data['status'] == 'OK'
        for field in fields:
            assert field in response.data

    def test_post_with_wrong_refresh_token(self):
        """
        Test: login by user with wrong refresh_token
        """
        user = mixer.blend(User)
        token = RefreshToken.for_user(user)
        request_data = {
            'grant_type': 'refresh_token',
            'refresh_token': str(token) + '1234',
        }
        url = reverse('GrantJWTTokenView')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = GrantJWTTokenView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['status'] == 'ERR'
        assert response.data['error'] == {'code': 400, 'msg': 'invalid token'}

    def test_post_with_wrong_password_email_phone(self):
        """
        Test: login by user with wrong password, email and phone
        """
        user = mixer.blend(User,
                           email='newuser@gmail.com',
                           phone='12345678',
                           password='test_password_1')
        user.set_password('test_password_1')
        user.save()
        request_data_cases = [
            {
                'grant_type': 'password',
                'login': user.email,
                'password': 'wrong_password',  # case with wrong password
            }, {
                'grant_type': 'password',
                'login': 'wrongmail@com.com',  # case with wrong email
                'password': 'test_password_1',
            }, {
                'grant_type': 'password',
                'login': '87654321',  # case with wrong phone
                'password': 'test_password_1',
            },
        ]
        url = reverse('GrantJWTTokenView')
        for request_data in request_data_cases:
            request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
            response = GrantJWTTokenView.as_view()(request=request)
            assert response.status_code == 400
            assert response.data['status'] == 'ERR'
            assert response.data['error'] == {'code': 400, 'msg': 'invalid credentials'}

    def test_post_with_wrong_grant_type(self):
        """
        Test: login by user with wrong grant_type
        """
        request_data = {
            'grant_type': 'wrong_grant_type',
        }
        url = reverse('GrantJWTTokenView')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = GrantJWTTokenView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['status'] == 'ERR'
        assert response.data['error'] == {'code': 400, 'msg': 'please specify grant_type, valid grant_type: password, refresh_token'}
