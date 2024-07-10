from django.test import TestCase, RequestFactory
from decimal import Decimal
from shop.models import Product, Category
from cart.cart import Cart

class CartTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = self.client.session
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product1 = Product.objects.create(
            category=self.category,
            name='Test Product 1',
            slug='test-product-1',
            price=Decimal('10.00'),
            available=True
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='Test Product 2',
            slug='test-product-2',
            price=Decimal('20.00'),
            available=True
        )
        self.cart = Cart(self.request)

    def test_add_product(self):
        self.cart.add(self.product1, quantity=1)
        self.assertIn(str(self.product1.id), self.cart.cart)
        self.assertEqual(self.cart.cart[str(self.product1.id)]['quantity'], 1)

    def test_add_multiple_products(self):
        self.cart.add(self.product1, quantity=1)
        self.cart.add(self.product2, quantity=2)
        self.assertEqual(len(self.cart), 3)
        self.assertEqual(self.cart.get_total_price(), Decimal('50.00'))

    def test_override_quantity(self):
        self.cart.add(self.product1, quantity=1)
        self.cart.add(self.product1, quantity=5, override_quantity=True)
        self.assertEqual(self.cart.cart[str(self.product1.id)]['quantity'], 5)

    def test_remove_product(self):
        self.cart.add(self.product1, quantity=1)
        self.cart.remove(self.product1)
        self.assertNotIn(str(self.product1.id), self.cart.cart)

    def test_get_total_price(self):
        self.cart.add(self.product1, quantity=1)
        self.cart.add(self.product2, quantity=2)
        self.assertEqual(self.cart.get_total_price(), Decimal('50.00'))

    def test_clear_cart(self):
        self.cart.add(self.product1, quantity=1)
        self.cart.clear()
        self.assertEqual(len(self.cart), 0)
