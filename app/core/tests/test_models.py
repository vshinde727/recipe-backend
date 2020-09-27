from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successfully(self):
        """Test creating new user with email successfully"""
        email = 'vivek@vivek.com'
        password = 'Changepass123'
        user = get_user_model().objects.create_user(
            email = email, 
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalise(self):
        """Test new user email is normalised"""
        email = "vivek@VIVEK.COM"
        user = get_user_model().objects.create_user(email = email)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test to check failure on invalid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Pwd12345')

    def test_create_new_super_user(self):
        """Test creation of super user"""
        user = get_user_model().objects.create_superuser(email='shvivek@vivek.com', password='1234Abcn')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)