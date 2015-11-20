import base64

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from noriv2api.models import User  # TODO: move to project level..


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user_dict = {
                'username': 'jacob',
                'email': 'jacob@web.de',
                'password': 'top_secret'
                }
        self.user = User.objects.create_user(**self.user_dict)

    def test_api_authentication_fail(self):
        url = reverse('user-authenticate')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_basic_authentication(self):
        url = reverse('user-authenticate')
        encoded_login = base64.b64encode(
            '{}:{}'.format(
                self.user_dict['username'],
                self.user_dict['password']).encode('ISO-8859-1'))
        self.client.credentials(HTTP_AUTHORIZATION=b'Basic ' + encoded_login)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user_dict['username'])

    def test_api_session_authentication(self):
        self.client.login(username=self.user_dict['username'],
                          password=self.user_dict['password'])
        url = reverse('user-authenticate')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user_dict['username'])