from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    """Clas to run tests on admin application"""

    def setUp(self): # setup fucntion is used to do some pre-req taks 
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(email='vivek@vivek.com', password='vivek')
        self.client.force_login(self.admin_user, backend=None)
        
        self.user = get_user_model().objects.create_user(email='user@vivek.com', password='password1234')

    def test_users_listed(self):
        """Test that users are listed on users page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        print(res)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the use edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_cereate_user_page(self):
        """Test create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)