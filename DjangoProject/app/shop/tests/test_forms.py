from django.test import SimpleTestCase
from shop.forms import ProductFilterForm


class ProductFilterFormTests(SimpleTestCase):
    def test_form_has_sort_by_field(self):
        form = ProductFilterForm()
        self.assertIn('sort_by', form.fields)

    def test_sort_by_field_choices(self):
        form = ProductFilterForm()
        choices = form.fields['sort_by'].choices
        self.assertEqual(choices, [
            ('asc', 'По возростанию цены'),
            ('desc', 'По убыванию цены'),
        ])

    def test_form_valid_data(self):
        form = ProductFilterForm(data={'sort_by': 'asc'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['sort_by'], 'asc')

    def test_form_valid_data_desc(self):
        form = ProductFilterForm(data={'sort_by': 'desc'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['sort_by'], 'desc')

    def test_form_empty_data(self):
        form = ProductFilterForm(data={'sort_by': ''})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['sort_by'], '')

    def test_form_invalid_data(self):
        form = ProductFilterForm(data={'sort_by': 'invalid'})
        self.assertFalse(form.is_valid())