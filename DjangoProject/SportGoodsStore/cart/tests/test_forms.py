from django.test import SimpleTestCase
from cart.forms import CartAddProductForm


class CartAddProductFormTestCase(SimpleTestCase):

    def test_form_fields(self):
        form = CartAddProductForm()
        self.assertIn('quantity', form.fields)
        self.assertIn('override', form.fields)

    def test_quantity_field_choices(self):
        form = CartAddProductForm()
        self.assertEqual(form.fields['quantity'].choices, [(i, str(i)) for i in range(1, 21)])

    def test_override_field_initial(self):
        form = CartAddProductForm()
        self.assertFalse(form.fields['override'].initial)

    def test_valid_data(self):
        form = CartAddProductForm(data={'quantity': '3', 'override': 'false'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['quantity'], 3)
        self.assertFalse(form.cleaned_data['override'])

    def test_invalid_quantity(self):
        form = CartAddProductForm(data={'quantity': '21', 'override': 'false'})
        self.assertFalse(form.is_valid())

    def test_override_hidden_field(self):
        form = CartAddProductForm(data={'quantity': '3', 'override': 'true'})
        self.assertEqual(form.fields['override'].widget.__class__.__name__, 'HiddenInput')
