from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from orders.models import Order, OrderItem
from shop.models import Product, Category
from cart.cart import Cart


class OrderCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('orders:order_create')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=10.00, category=self.category)

        self.form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'Test City',
            'phone': '1234567890',
        }

    @patch('orders.tasks.order_created')
    def test_create_order_success(self, mock_order_created):
        cart = Cart(self.client.session)
        cart.add(product=self.product, quantity=1)

        response = self.client.post(self.url, self.form_data)

        self.assertRedirects(response, reverse('orders:order_created'))

        self.assertTrue(Order.objects.exists())
        order = Order.objects.get(email='john.doe@example.com')
        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.last_name, 'Doe')
        self.assertEqual(order.address, '123 Main St')
        self.assertEqual(order.postal_code, '12345')
        self.assertEqual(order.city, 'Test City')
        self.assertEqual(order.phone, '1234567890')
        self.assertFalse(order.paid)

        self.assertTrue(OrderItem.objects.exists())
        order_item = OrderItem.objects.get(order=order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.price, self.product.price)
        self.assertEqual(order_item.quantity, 1)

        mock_order_created.delay.assert_called_once_with(order.id)

    def test_create_order_invalid_form(self):
        invalid_form_data = self.form_data.copy()
        invalid_form_data['email'] = 'invalid-email'

        response = self.client.post(self.url, invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order/create.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)


        self.assertFalse(Order.objects.exists())
        self.assertFalse(OrderItem.objects.exists())

    def test_create_order_empty_cart(self):
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, reverse('cart:cart_detail'))


        self.assertFalse(Order.objects.exists())
        self.assertFalse(OrderItem.objects.exists())
