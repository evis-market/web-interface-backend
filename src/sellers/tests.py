import json
import pytest
from django.core.files import File
from django.forms import model_to_dict
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from sellers.models import Contact, Seller
from sellers.views import SellerSettingsView
from upload.models import UploadedFile
from users.models import User

pytestmark = pytest.mark.django_db


class TestSellerSettingsView:

    def test_get(self):
        """
        Test: get seller with contacts
        Returns:

        """
        user = mixer.blend(User)
        seller = mixer.blend(Seller,
                             seller=user,
                             logo_url=File(open("test-files/test-logo.png", 'rb')))
        url_contact = mixer.blend(Contact,
                                  seller=seller,
                                  type_id=Contact.TYPE_ID_URL,
                                  value='https://domain1.com/',
                                  comment='Test URL contact')
        phone_contact = mixer.blend(Contact,
                                    seller=seller,
                                    type_id=Contact.TYPE_ID_PHONE,
                                    value='1234567',
                                    comment='Test phone contact')
        email_contact = mixer.blend(Contact,
                                    seller=seller,
                                    type_id=Contact.TYPE_ID_EMAIL,
                                    value='email2@test.com',
                                    comment='Test email contact')
        url = reverse('SellerSettingsView')
        request = APIRequestFactory().get(url)
        force_authenticate(request, user=user)
        response = SellerSettingsView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'
        seller = Seller.objects.get(seller=user)
        seller_fields = {
            'name': seller.name,
            'descr': seller.descr,
            'logo_url': f'http://testserver{seller.logo_url.url}',
            'wallet_for_payments_erc20': seller.wallet_for_payments_erc20,
            'rating': seller.rating
        }
        url_response_contacts = response.data['seller']['contacts'][0]
        phone_response_contacts = response.data['seller']['contacts'][1]
        email_response_contacts = response.data['seller']['contacts'][2]
        url_contact, phone_contact, email_contact = model_to_dict(url_contact), model_to_dict(phone_contact), model_to_dict(email_contact)

        for key, value in seller_fields.items():
            if key == 'contacts':
                for _key, _value in url_response_contacts.items():
                    assert url_contact[_key] == _value
                for _key, _value in phone_response_contacts.items():
                    assert phone_contact[_key] == _value
                for _key, _value in email_response_contacts.items():
                    assert email_contact[_key] == _value
            assert response.data['seller'][key] == value

    def test_put_create(self):
        """
        Test: create new seller with contacts
        """
        user = mixer.blend(User)
        file = mixer.blend(UploadedFile,
                           file=File(open("../sellers/test-files/test-logo.png", 'rb')),
                           file_name_original='test-logo',
                           created_by=user)
        url = reverse('SellerSettingsView')
        data = {
            'seller': user.id,
            'name': 'Seller name',
            'descr': 'Seller description',
            'logo_url': str(file.uuid),
            'wallet_for_payments_erc20': '0xC88E53eda9A20C9aE52e8a222f1a56793188d196',
            'contacts': [
                {'type': 1, 'value': 'https://domain1.com/', 'comment': 'main site'},
                {'type': 2, 'value': '12312312311', 'comment': 'phone1 comment'},
                {'type': 3, 'value': 'email1@test.com', 'comment': 'email1 comment'},
            ],
        }
        request = APIRequestFactory().put(url, data=json.dumps(data), content_type='application/json')
        force_authenticate(request, user=user)
        response = SellerSettingsView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'
        seller = Seller.objects.get_seller_by_user_id(user_id=user.id)
        url_contact, phone_contact, email_contact = Contact.objects.get_all_by_seller(seller=seller)
        seller = model_to_dict(seller)
        url_contact, phone_contact, email_contact = model_to_dict(url_contact), model_to_dict(phone_contact), model_to_dict(email_contact)
        for key, value in data.items():
            if key == 'contacts':
                for _key, _value in data['contacts'][0].items():
                    assert url_contact[_key] == _value
                for _key, _value in data['contacts'][1].items():
                    assert phone_contact[_key] == _value
                for _key, _value in data['contacts'][2].items():
                    assert email_contact[_key] == _value
            elif key == 'logo_url':
                assert str(seller[key]) == f'seller_logo/{file.uuid}.png'
            else:
                assert seller[key] == value

    def test_put_update(self):
        """
        Test: update old seller information and his contacts
        Returns:

        """
        user = mixer.blend(User)
        seller = mixer.blend(Seller,
                             seller=user,
                             logo_url='')
        file = mixer.blend(UploadedFile,
                           file=File(open("../sellers/test-files/test-logo.png", 'rb')),
                           file_name_original='test-logo',
                           created_by=user)
        old_contact = mixer.blend(Contact,
                                  seller=seller)
        url = reverse('SellerSettingsView')
        data = {
            'seller': user.id,
            'name': 'New seller name',
            'descr': 'New seller description',
            'logo_url': str(file.uuid),
            'wallet_for_payments_erc20': '0x....',
            'contacts': [
                {'type': 1, 'value': 'https://domain1.com/', 'comment': 'main site'},
                {'type': 2, 'value': '12312311231', 'comment': 'phone1 comment'},
                {'type': 3, 'value': 'email1@test.com', 'comment': 'email1 comment'},
            ],
        }
        request = APIRequestFactory().put(url, data=json.dumps(data), content_type='application/json')
        force_authenticate(request, user=user)
        response = SellerSettingsView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'
        seller = Seller.objects.get_seller_by_user_id(user_id=user.id)
        url_contact, phone_contact, email_contact = Contact.objects.get_all_by_seller(seller=seller)
        seller = model_to_dict(seller)
        url_contact, phone_contact, email_contact = model_to_dict(url_contact), model_to_dict(phone_contact), model_to_dict(email_contact)
        for key, value in data.items():
            if key == 'contacts':
                for _key, _value in data['contacts'][0].items():
                    assert url_contact[_key] == _value
                for _key, _value in data['contacts'][1].items():
                    assert phone_contact[_key] == _value
                for _key, _value in data['contacts'][2].items():
                    assert email_contact[_key] == _value
            elif key == 'logo_url':
                assert str(seller[key]) == f'seller_logo/{file.uuid}.png'
            else:
                assert seller[key] == value
        with pytest.raises(Contact.DoesNotExist):
            Contact.objects.get(id=old_contact.id)

    def test_put_create_with_invalid_fields(self):
        """
        Test: create new seller with invalid contacts
        """
        user = mixer.blend(User)
        url = reverse('SellerSettingsView')
        data = {
            'seller': user.id,
            'name': 'New seller name',
            'contacts': [
                {'type': Contact.TYPE_ID_PHONE, 'value': '131231231', 'comment': 'phone1 comment'},
                {'type': Contact.TYPE_ID_PHONE, 'value': '12312d31231', 'comment': 'phone2 comment'},
                {'type': Contact.TYPE_ID_EMAIL, 'value': 'email1#test.com', 'comment': 'email1 comment'},
                {'type': Contact.TYPE_ID_EMAIL, 'value': 'email1@test.com', 'comment': 'email2 comment'},
                {'type': Contact.TYPE_ID_URL, 'value': 'domain1.com', 'comment': 'main site'},
            ],
        }
        request = APIRequestFactory().put(url, data=json.dumps(data), content_type='application/json')
        force_authenticate(request, user=user)
        response = SellerSettingsView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert response.data['status'] == 'ERR'
        assert 'msg' in response.data['error']
        print(response)
        print(response.data)
        assert 0 in response.data['error']['invalid_fields']['contacts']
        assert 1 in response.data['error']['invalid_fields']['contacts']
        assert 2 in response.data['error']['invalid_fields']['contacts']
        assert 4 in response.data['error']['invalid_fields']['contacts']

    def test_put_create_without_contacts(self):
        """
        Test: create new seller without contacts
        """
        user = mixer.blend(User)
        url = reverse('SellerSettingsView')
        data = {
            'seller': user.id,
            'name': 'New seller name',
            'contacts': [],
        }
        request = APIRequestFactory().put(url, data=json.dumps(data), content_type='application/json')
        force_authenticate(request, user=user)
        response = SellerSettingsView.as_view()(request=request)
        assert response.status_code == 400
        assert response.data['error']['code'] == 400
        assert response.data['status'] == 'ERR'
        assert 'msg' in response.data['error']
        assert 'contacts' in response.data['error']['invalid_fields']
