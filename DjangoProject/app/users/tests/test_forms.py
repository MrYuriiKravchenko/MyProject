from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User
from PIL import Image
import io


def get_temporary_image():
    """Создает временное изображение для тестов."""
    image = Image.new('RGB', (100, 100))
    tmp_file = io.BytesIO()
    image.save(tmp_file, 'jpeg')
    tmp_file.seek(0)
    return SimpleUploadedFile(name='test_image.jpg', content=tmp_file.read(), content_type='image/jpeg')


class CustomUserCreationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'phone_number': '1234567890',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        image_data = get_temporary_image()
        form = CustomUserCreationForm(data=form_data, files={'image': image_data})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'email': 'invalid-email',
            'username': '',
            'phone_number': 'invalid-phone',
            'first_name': '',
            'last_name': '',
            'password1': '123',
            'password2': '1234',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        if 'username' in form.fields:
            self.assertIn('username', form.errors)
        if 'phone_number' in form.errors:
            self.assertIn('phone_number', form.errors)
        if 'password2' in form.errors:
            self.assertIn('password2', form.errors)


class CustomUserChangeFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='complexpassword123'
        )

    def test_valid_form(self):
        form_data = {
            'email': 'newemail@example.com',
            'username': 'newusername',
            'phone_number': '0987654321',
            'first_name': 'New',
            'last_name': 'User',
        }
        image_data = get_temporary_image()
        form = CustomUserChangeForm(instance=self.user, data=form_data, files={'image': image_data})
        self.assertTrue(form.is_valid(), form.errors.as_json())

    def test_invalid_form(self):
        form_data = {
            'email': 'invalid-email',
            'username': '',
            'phone_number': 'invalid-phone',
            'first_name': '',
            'last_name': '',
        }
        form = CustomUserChangeForm(instance=self.user, data=form_data)
        self.assertIn('email', form.errors)
        if 'username' in form.fields:
            self.assertIn('username', form.errors)
        if 'phone_number' in form.errors:
            self.assertIn('phone_number', form.errors)
