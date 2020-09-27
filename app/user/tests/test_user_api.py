from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """Test the users api public"""
    def setUp(self):
        self.client = APIClient() 
    
    def test_create_valid_user_success(self):
        """Test creataing user with valid payload is successful"""
        payload = {
            "email": "test@dev.com",
            "name": "Test Name",
            "password": "testpass"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Check if user exists"""
        payload = {
            "email": "test@dev.com",
            "name": "Test Name",
            "password": "testpass"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test password more than 5 chars"""
        payload = {
            "email": "test@dev.com",
            "name": "Test Name",
            "password": "pwd"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)        
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for the user"""
        payload = {
            "email": "test@dev.com",
            "name": "Test Name",
            "password": "testpass"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Token should not be created if password is incorrect"""
        payload1 = {
            "email": "test@dev.com",
            "name": "Test Name",
            "password": "testpass"
        }
        payload2 = {
            "email": "test@dev.com",
            "name": "Test Name",
            "password": "testpass1"
        }
        create_user(**payload1)
        res = self.client.post(TOKEN_URL, payload2)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user(self):
        """Test that token is not created if the user does not exists"""
        payload2 = {
            "email": "test1@dev.com",
            "name": "Test Name",
            "password": "testpass"
        }
        res = self.client.post(TOKEN_URL, payload2)
        print(res)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_password(self):
        """Test that token is not created if the user does not exists"""
        payload2 = { "email": "test1@dev.com", 'password':'' }
        res = self.client.post(TOKEN_URL, payload2)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
        
