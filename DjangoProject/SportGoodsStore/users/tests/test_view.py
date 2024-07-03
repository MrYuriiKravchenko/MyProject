from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.contrib.messages import get_messages
from django.urls import reverse
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User

User = get_user_model()


class UserViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('users:signup')
        self.profile_url = reverse('users:profile')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_signup_view_post_success(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_profile_view_get(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsInstance(response.context['form'], CustomUserChangeForm)
        self.assertEqual(response.context['form'].instance, self.user)

    def test_profile_view_post_success(self):
        response = self.client.post(self.profile_url, {
            'username': 'updateduser',
            'phone_number': '1234567890'
        })
        self.assertRedirects(response, self.profile_url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.phone_number, '1234567890')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ваш профиль успешно обновлен')

    def test_profile_view_post_invalid(self):
        response = self.client.post(self.profile_url, {
            'username': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, 'Пожалуйста, исправте ошибки в форме')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Пожалуйста, исправте ошибки в форме')
