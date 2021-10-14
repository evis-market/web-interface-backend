import json
import pytest
from django.forms import model_to_dict
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from sellers.models import Contact, Seller
from sellers.views import SellerSettingsView
from users.models import User


pytestmark = pytest.mark.django_db


class TestSellerSettingsView:

    def test_get(self):
        user = mixer.blend(User)
        seller = mixer.blend(Seller,
                             seller_id=user)
        url_contact = mixer.blend(Contact,
                                  seller_id=seller,
                                  type_id=Contact.TYPE_ID_URL,
                                  value='https://domain1.com/',
                                  comment='Test URL contact')
        phone_contact = mixer.blend(Contact,
                                    seller_id=seller,
                                    type_id=Contact.TYPE_ID_PHONE,
                                    value='1234567',
                                    comment='Test phone contact')
        email_contact = mixer.blend(Contact,
                                    seller_id=seller,
                                    type_id=Contact.TYPE_ID_EMAIL,
                                    value='email2@test.com',
                                    comment='Test email contact')
        url = reverse('SellerSettingsView')
        request = APIRequestFactory().get(url)
        force_authenticate(request, user=user)
        response = SellerSettingsView.as_view()(request=request)
        assert response.status_code == 200
        url_response_contacts = response.data['seller']['contacts'][0]
        phone_response_contacts = response.data['seller']['contacts'][1]
        email_response_contacts = response.data['seller']['contacts'][2]
        for key, value in model_to_dict(seller).items():
            assert response.data['seller'][key] == value
        for key, value in model_to_dict(url_contact).items():
            assert url_response_contacts[key] == value
        for key, value in model_to_dict(phone_contact).items():
            assert phone_response_contacts[key] == value
        for key, value in model_to_dict(email_contact).items():
            assert email_response_contacts[key] == value

    def test_put_create(self):
        user = mixer.blend(User)
        url = reverse('SellerSettingsView')
        data = {
            'seller_id': user.id,
            'name': 'Seller name',
            'description': 'Seller description',
            'logo_url': 'https://www.goog.ru/',
            'wallet_for_payments_erc20': '0x....',
            'contacts': [
                {'type_id': 1, 'value': 'https://domain1.com/', 'comment': 'main site'},
                {'type_id': 2, 'value': '1231231231', 'comment': 'phone1 comment'},
                {'type_id': 3, 'value': 'email1@test.com', 'comment': 'email1 comment'},
            ],
        }
        request = APIRequestFactory().put(url, data=json.dumps(data), content_type='application/json')
        force_authenticate(request, user=user)
        response = SellerSettingsView.as_view()(request=request)
        assert response.status_code == 200
        seller = Seller.objects.get_seller_by_user_id(user_id=user.id)
        url_contact, phone_contact, email_contact = Contact.objects.get_all_by_seller(seller_id=seller.id)
        for key, value in data.items():
            if key == 'contacts':
                for k, v in data['contacts'][0].items():
                    assert model_to_dict(url_contact)[k] == v
                for i, j in data['contacts'][1].items():
                    assert model_to_dict(phone_contact)[i] == j
                for x, y in data['contacts'][2].items():
                    assert model_to_dict(email_contact)[x] == y
            else:
                assert model_to_dict(seller)[key] == value

    def test_put_update(self):
        user = mixer.blend(User)
        seller = mixer.blend(Seller,
                             seller_id=user)
        old_contact = mixer.blend(Contact,
                                  seller_id=seller)
        url = reverse('SellerSettingsView')
        data = {
            'seller_id': user.id,
            'name': 'New seller name',
            'description': 'New seller description',
            'logo_url': 'https://www.goog.ru/',
            'wallet_for_payments_erc20': '0x....',
            'contacts': [
                {'type_id': 1, 'value': 'https://domain1.com/', 'comment': 'main site'},
                {'type_id': 2, 'value': '1231231231', 'comment': 'phone1 comment'},
                {'type_id': 3, 'value': 'email1@test.com', 'comment': 'email1 comment'},
            ],
        }
        request = APIRequestFactory().put(url, data=json.dumps(data), content_type='application/json')
        force_authenticate(request, user=user)
        response = SellerSettingsView.as_view()(request=request)
        assert response.status_code == 200
        seller = Seller.objects.get_seller_by_user_id(user_id=user.id)
        url_contact, phone_contact, email_contact = Contact.objects.get_all_by_seller(seller_id=seller.id)
        for key, value in data.items():
            if key == 'contacts':
                for k, v in data['contacts'][0].items():
                    assert model_to_dict(url_contact)[k] == v
                for i, j in data['contacts'][1].items():
                    assert model_to_dict(phone_contact)[i] == j
                for x, y in data['contacts'][2].items():
                    assert model_to_dict(email_contact)[x] == y
            else:
                assert model_to_dict(seller)[key] == value
        with pytest.raises(Contact.DoesNotExist):
            Contact.objects.get(id=old_contact.id)
