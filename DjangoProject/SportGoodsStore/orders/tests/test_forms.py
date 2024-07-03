from django.test import TestCase
from orders.forms import OrderCreateForm
from orders.models import Order


class OrderCreateFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'ivan@example.com',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'Москва',
            'phone': '1234567890'
        }
        form = OrderCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertEqual(order.first_name, form_data['first_name'])
        self.assertEqual(order.last_name, form_data['last_name'])
        self.assertEqual(order.email, form_data['email'])
        self.assertEqual(order.address, form_data['address'])
        self.assertEqual(order.postal_code, form_data['postal_code'])
        self.assertEqual(order.city, form_data['city'])
        self.assertEqual(order.phone, form_data['phone'])

    def test_invalid_form_missing_fields(self):
        form_data = {
            'first_name': 'Иван',
            'email': 'ivan@example.com',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'Москва'
        }
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertIn('last_name', form.errors)

    def test_invalid_form_invalid_email(self):
        form_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'not-an-email',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'Москва',
            'phone': '1234567890'
        }
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalid_form_missing_email(self):
        form_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'Москва',
            'phone': '1234567890'
        }
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
