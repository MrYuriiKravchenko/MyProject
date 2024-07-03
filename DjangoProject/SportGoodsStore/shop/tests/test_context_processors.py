from django.test import RequestFactory, TestCase
from shop.context_processors import breadcrumbs


class BreadcrumbsContextProcessorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_breadcrumbs_home(self):
        request = self.factory.get('/')
        context = breadcrumbs(request)
        expected = [{'name': 'Home', 'url': '/'}]
        self.assertEqual(context['breadcrumbs'], expected)

    def test_breadcrumbs_category(self):
        request = self.factory.get('/category/')
        context = breadcrumbs(request)
        expected = [
            {'name': 'Home', 'url': '/'},
            {'name': 'Category', 'url': '/category/'}
        ]
        self.assertEqual(context['breadcrumbs'], expected)

    def test_breadcrumbs_product(self):
        request = self.factory.get('/category/product/')
        context = breadcrumbs(request)
        expected = [
            {'name': 'Home', 'url': '/'},
            {'name': 'Category', 'url': '/category/'},
            {'name': 'Product', 'url': '/category/product/'}
        ]
        self.assertEqual(context['breadcrumbs'], expected)
