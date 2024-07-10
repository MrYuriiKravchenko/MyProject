from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from shop.models import Category, Product, Wishlist
from django.test import TestCase, Client


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
        self.product = Product.objects.create(name='Product1', slug='product1', category=self.category, available=True,
                                              price=20.00)
        self.unavailable_product = Product.objects.create(name='Product2', slug='product2', category=self.category,
                                                          available=False, price=30.00)

    def test_product_detail_view(self):
        response = self.client.get(reverse('shop:product_detail', args=[self.product.id, self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/detail.html')
        self.assertContains(response, self.product.name)

    def test_product_detail_view_unavailable_product(self):
        response = self.client.get(
            reverse('shop:product_detail', args=[self.unavailable_product.id, self.unavailable_product.slug]))
        self.assertEqual(response.status_code, 404)


class SearchResultsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Electronics', slug='electronics')

        self.product1 = Product.objects.create(
            category=self.category,
            name='Laptop',
            slug=slugify('Laptop'),
            price=1000,
            available=True
        )

        self.product2 = Product.objects.create(
            category=self.category,
            name='Smartphone',
            slug=slugify('Smartphone'),
            price=800,
            available=True
        )

        self.product3 = Product.objects.create(
            category=self.category,
            name='Tablet',
            slug=slugify('Tablet'),
            price=600,
            available=True
        )

    def test_search_results(self):
        response = self.client.get(reverse('shop:search_results'), {'q': 'Laptop'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/search_results.html')
        self.assertContains(response, 'Laptop')
        self.assertNotContains(response, 'Smartphone')
        self.assertNotContains(response, 'Tablet')
        self.assertEqual(len(response.context['product_list']), 1)

    def test_search_no_results(self):
        response = self.client.get(reverse('shop:search_results'), {'q': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/search_results.html')
        self.assertContains(response, 'No products found')
        self.assertEqual(len(response.context['product_list']), 0)

    def test_search_empty_query(self):
        response = self.client.get(reverse('shop:search_results'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/search_results.html')
        self.assertEqual(len(response.context['product_list']), 0)

    def test_search_pagination(self):
        response = self.client.get(reverse('shop:search_results'), {'q': 'a', 'page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/search_results.html')
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['product_list']), 3)


User = get_user_model()


class WishlistViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='TestCategory', slug='test-category')

        self.product1 = Product.objects.create(
            category=self.category,
            name='Test Product 1',
            slug='test-product-1',
            price=100.00,
            available=True
        )

        self.product2 = Product.objects.create(
            category=self.category,
            name='Test Product 2',
            slug='test-product-2',
            price=200.00,
            available=True
        )

        self.wishlist_item1 = Wishlist.objects.create(user=self.user, product=self.product1)
        self.wishlist_item2 = Wishlist.objects.create(user=self.user, product=self.product2)

        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_wishlist_view_status_code(self):
        response = self.client.get(reverse('shop:wishlist'))
        self.assertEqual(response.status_code, 200)

    def test_wishlist_view_template_used(self):
        response = self.client.get(reverse('shop:wishlist'))
        self.assertTemplateUsed(response, 'shop/wishlist.html')

    def test_wishlist_view_context_data(self):
        response = self.client.get(reverse('shop:wishlist'))
        self.assertTrue('wishlist_items' in response.context)
        self.assertEqual(len(response.context['wishlist_items']), 2)
        self.assertIn(self.wishlist_item1, response.context['wishlist_items'])
        self.assertIn(self.wishlist_item2, response.context['wishlist_items'])

    def test_wishlist_view_unauthenticated_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('shop:wishlist'))
        self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('shop:wishlist')}")