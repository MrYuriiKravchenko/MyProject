from django.test import TestCase
from django.urls import reverse

from shop.models import Category, Product


class ProductListViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category1', slug='category1')
        self.product1 = Product.objects.create(name='Product1', slug='product1', category=self.category, available=True,
                                               price=10.00)
        self.product2 = Product.objects.create(name='Product2', slug='product2', category=self.category, available=True,
                                               price=20.00)
        self.product3 = Product.objects.create(name='Product3', slug='product3', category=self.category,
                                               available=False, price=30.00)

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)
        self.assertNotContains(response, self.product3.name)

    def test_product_list_view_with_category(self):
        response = self.client.get(reverse('shop:product_list_by_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)
        self.assertNotContains(response, self.product3.name)
        self.assertEqual(response.context['category'], self.category)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category1', slug='category1')
        self.product = Product.objects.create(name='Product1', slug='product1', category=self.category, available=True, price=20.00)
        self.unavailable_product = Product.objects.create(name='Product2',slug='product2', category=self.category, available=False, price=30.00)

    def test_product_detail_view(self):
        response = self.client.get(reverse('shop:product_detail', args=[self.product.id, self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/detail.html')
        self.assertContains(response, self.product.name)

    def test_product_detail_view_unavailable_product(self):
        response = self.client.get(reverse('shop:product_detail', args=[self.unavailable_product.id, self.unavailable_product.slug]))
        self.assertEqual(response.status_code, 404)