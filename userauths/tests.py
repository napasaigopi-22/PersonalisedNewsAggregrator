from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class UserAuthTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
        self.user.save()

    def test_user_creation(self):
        user = User.objects.create_user(username='newuser', password='password123', email='new@example.com')
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('password123'))

    def test_user_login(self):
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)

    def test_user_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_update(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('profile_update'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'bio': 'Updated bio'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.bio, 'Updated bio')

    def test_user_login_with_wrong_password(self):
        login = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(login)

    def test_user_login_with_nonexistent_username(self):
        login = self.client.login(username='nonexistent', password='password123')
        self.assertFalse(login)

    def test_user_creation_without_username(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', password='password123', email='test@example.com')

    def test_user_creation_without_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='testuser2', password='', email='test2@example.com')

    def test_user_creation_without_email(self):
        user = User.objects.create_user(username='testuser3', password='password123')
        self.assertEqual(user.email, '')

    def test_duplicate_user_creation(self):
        with self.assertRaises(Exception):
            User.objects.create_user(username='testuser', password='password123', email='test@example.com')

    def test_user_profile_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_user_password_change(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('password_change'), {
            'old_password': 'password123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_user_password_reset(self):
        response = self.client.post(reverse('password_reset'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)

    def test_user_password_reset_invalid_email(self):
        response = self.client.post(reverse('password_reset'), {'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No account found with that email address.')

    def test_user_deletion(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='testuser')
