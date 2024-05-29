from django.test import TestCase
from django.db import IntegrityError
from shop.models import Category


class ProductModelTests(TestCase):
    """Создаем тестовый объект категории"""

    def setUp(self):
        self.category = Category.objects.create(
            name='Штанги',
            slug='test-category'
        )

    def test_create_category(self):
        """Проверяем, что объект был успешно создан"""
        self.assertEqual(self.category.name, 'Штанги')
        self.assertEqual(self.category.slug, 'test-category')

    def test_string_representation(self):
        """Проверяем строковое представление объекта"""
        self.assertEqual(str(self.category), self.category.name)

    def test_unique_slug(self):
        """Проверяем уникальность поля slug"""
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name='Другие категории',
                slug='test-category'  # тот же slug, что и у self.category
            )

    def test_ordering(self):
        """Проверяем порядок сортировки"""
        category1 = Category.objects.create(name='A Category', slug='a-category')
        category2 = Category.objects.create(name='B Category', slug='b-category')
        categories = Category.objects.all().order_by('name')
        self.assertEqual(categories[0], category1)
        self.assertEqual(categories[1], category2)
        self.assertEqual(categories[2], self.category)
