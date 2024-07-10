from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from shop.models import Category, Product


class CartViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='TestCategory', slug='testcategory')
        self.product = Product.objects.create(
            category=self.category,
            name='TestProduct',
            slug='testproduct',
            price=Decimal('10.00'),
            available=True
        )
        self.cart_add_url = reverse('cart:cart_add', args=[self.product.id])
        self.cart_remove_url = reverse('cart:cart_remove', args=[self.product.id])
        self.cart_detail_url = reverse('cart:cart_detail')

    def test_cart_add_view(self):
        form_data = {
            'quantity': 1,
            'override': False
        }
        response = self.client.post(self.cart_add_url, form_data)
        self.assertRedirects(response, reverse('cart:cart_detail'))
        session = self.client.session
        cart = session.get('cart')
        self.assertIsNotNone(cart)
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)]['quantity'], 1)

    def test_cart_remove_view(self):
        self.client.post(self.cart_add_url, {'quantity': 1, 'override': False})
        response = self.client.post(self.cart_remove_url)
        self.assertRedirects(response, self.cart_detail_url)
        session = self.client.session
        cart = session.get('cart')
        self.assertIsNotNone(cart)
        self.assertNotIn(str(self.product.id), cart)

    def test_cart_detail_view(self):
        self.client.post(self.cart_add_url, {'quantity': 1, 'override': False})
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertIn('cart', response.context)
        cart = response.context['cart']
        cart_items = [item for item in cart]
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0]['product'], self.product)
        self.assertEqual(cart_items[0]['quantity'], 1)