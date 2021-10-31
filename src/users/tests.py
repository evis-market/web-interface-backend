import json
import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from users.models import User
from users.views import SignupView

pytestmark = pytest.mark.django_db


class TestSignupView:

    def test_post_normal_signup(self):
        """
        Test: normal signup with all and valid fields
        """
        request_data = {
            "first_name": "John",
            "last_name": "Smith",
            "phone": "15552223456",
            "email": "test@test.com",
            "wallet_erc20": "0xC88E53eda9A20C9aE52e8a222f1a56793188d196",
            "password": "some_very_strong_password"
        }
        url = reverse('signup')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = SignupView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['user_id'] == 1
        assert response.data['status'] == 'OK'
        user = User.objects.get(first_name=request_data['first_name'],
                                last_name=request_data['last_name'],
                                phone=request_data['phone'],
                                email=request_data['email'],
                                wallet_erc20=request_data['wallet_erc20'])
        assert user.password is not None and user.password != request_data['password']

    def test_post_with_only_one_required_field_and_password(self):
        """
        Test: signup with only one required field and password

        case 1: signup with phone only
        case 2: signup with email only
        case 3: signup with wallet_erc20 only
        """
        request_data_cases = [
            {
                "phone": "15552223456",
                "password": "some_very_strong_password"
            },
            {
                "email": "test@test.com",
                "password": "some_very_strong_password"
            },
            {
                "wallet_erc20": "0xC88E53eda9A20C9aE52e8a222f1a56793188d196",
                "password": "some_very_strong_password"
            },
        ]
        url = reverse('signup')
        user_id = 1
        for request_data in request_data_cases:
            request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
            response = SignupView.as_view()(request=request)
            assert response.status_code == 200
            assert response.data['user_id'] == user_id
            assert response.data['status'] == 'OK'
            user_id += 1

    def test_post_signup_without_password(self):
        """
        Test: signup without password
        """
        request_data = {
            "phone": "15552223456",
            "email": "test@test.com",
            "wallet_erc20": "0xC88E53eda9A20C9aE52e8a222f1a56793188d196",
        }
        url = reverse('signup')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = SignupView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert 'msg' in response.data['error']
        assert 'password' in response.data['error']['invalid_fields']
        assert response.data['status'] == 'ERR'

    def test_post_signup_with_invalid_password(self):
        """
        Test: signup with invalid password
        """
        request_data = {
            "phone": "15552223456",
            "password": "1111"
        }
        url = reverse('signup')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = SignupView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert 'msg' in response.data['error']
        assert 'password' in response.data['error']['invalid_fields']
        assert response.data['status'] == 'ERR'

    def test_post_signup_with_not_unique_phone(self):
        """
        Test: signup with not unique phone
        """
        mixer.blend(User,
                    phone='15552223456')
        request_data = {
            "phone": "15552223456",
            "password": "some_very_strong_password"
        }
        url = reverse('signup')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = SignupView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert 'msg' in response.data['error']
        assert 'phone' in response.data['error']['invalid_fields']
        assert response.data['status'] == 'ERR'

    def test_post_signup_with_not_unique_email(self):
        """
        Test: signup with not unique email
        """
        mixer.blend(User,
                    email="test@test.com")
        request_data = {
            "email": "test@test.com",
            "password": "some_very_strong_password"
        }
        url = reverse('signup')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = SignupView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert 'msg' in response.data['error']
        assert 'email' in response.data['error']['invalid_fields']
        assert response.data['status'] == 'ERR'

    def test_post_signup_with_not_unique_wallet_erc20(self):
        """
        Test: signup with not unique wallet_erc20
        """
        mixer.blend(User,
                    wallet_erc20="0xC88E53eda9A20C9aE52e8a222f1a56793188d196")
        request_data = {
            "wallet_erc20": "0xC88E53eda9A20C9aE52e8a222f1a56793188d196",
            "password": "some_very_strong_password"
        }
        url = reverse('signup')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = SignupView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert 'msg' in response.data['error']
        assert 'wallet_erc20' in response.data['error']['invalid_fields']
        assert response.data['status'] == 'ERR'

    def test_post_signup_with_invalid_phone_case_min_length(self):
        """
        Test: signup with invalid MIN_PHONE_LENGTH
        """
        request_data = {
            "phone": "123456789101234567890"[:User.MIN_PHONE_LENGTH - 1],
            "password": "some_very_strong_password"
        }
        url = reverse('signup')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = SignupView.as_view()(request=request)
        assert len(request_data['phone']) < User.MIN_PHONE_LENGTH
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert 'msg' in response.data['error']
        assert 'phone' in response.data['error']['invalid_fields']
        assert response.data['status'] == 'ERR'

    def test_post_signup_with_invalid_phone_case_max_length(self):
        """
        Test: signup with invalid MAX_PHONE_LENGTH
        """
        request_data = {
            "phone": "123456789101234567890"[:User.MAX_PHONE_LENGTH + 1],
            "password": "some_very_strong_password"
        }
        url = reverse('signup')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = SignupView.as_view()(request=request)
        assert len(request_data['phone']) > User.MAX_PHONE_LENGTH
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert 'msg' in response.data['error']
        assert 'phone' in response.data['error']['invalid_fields']
        assert response.data['status'] == 'ERR'

    def test_post_signup_with_invalid_wallet_erc20(self):
        """
        Test: signup with invalid wallet_erc20

        case 1: the wallet_erc20 not start with 0x
        case 2: invalid length less then 42
        """
        request_data_cases = [
            {
                "wallet_erc20": "1xC88E53eda9A20C9aE52e8a222f1a56793188d196",
                "password": "some_very_strong_password"
            },
            {
                "wallet_erc20": "0xC88E53eda9A20C9aE5",
                "password": "some_very_strong_password"
            },
        ]
        url = reverse('signup')
        for request_data in request_data_cases:
            request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
            response = SignupView.as_view()(request=request)
            assert response.status_code == 400
            assert response.data['error']['code'] == 400
            assert 'msg' in response.data['error']
            assert 'wallet_erc20' in response.data['error']['invalid_fields']
            assert response.data['status'] == 'ERR'

    def test_post_signup_with_invalid_wallet_erc20_case_with_wrong_chars(self):
        """
        Test: signup with invalid wallet_erc20 where wallet_erc20 has some wrong char
        """
        request_data = {
            "wallet_erc20": "0xC8853eda9A20C9aE52e8a222f1a56793188d196G",
            "password": "some_very_strong_password"
        }
        url = reverse('signup')
        wrong_chars = ['-', '.', ';', ':', '\\', '|', '?', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '{', '}', '"', "'", '`', '+']
        for char in wrong_chars:
            request_data['wallet_erc20'].replace('G', char)
            request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
            response = SignupView.as_view()(request=request)
            assert response.status_code == 400
            assert response.data['error']['code'] == 400
            assert 'msg' in response.data['error']
            assert 'wallet_erc20' in response.data['error']['invalid_fields']
            assert response.data['status'] == 'ERR'

    def test_post_signup_with_invalid_wallet_erc20_case_with_length_more_then_42(self):
        """
        Test: signup with invalid wallet_erc20 where length more then 42
        """
        request_data = {
            "wallet_erc20": "0xC8853eda9A20C9aE52e8a222f1a56793188d196G11",
            "password": "some_very_strong_password"
        }
        url = reverse('signup')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        response = SignupView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert 'msg' in response.data['error']
        assert 'wallet_erc20' in response.data['error']['invalid_fields']
        assert response.data['status'] == 'ERR'
