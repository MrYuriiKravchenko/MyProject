from django.test import TestCase
from coupons.forms import CouponApplyForm


class CouponApplyFormTest(TestCase):
    def test_form_valid_data(self):
        form = CouponApplyForm(data={'code': 'SUMMER2024'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['code'], 'SUMMER2024')

    def test_form_empty_data(self):
        form = CouponApplyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('code' in form.errors)

    def test_form_invalid_data(self):
        form = CouponApplyForm(data={'code': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('code' in form.errors)

    def test_form_whitespace_code(self):
        form = CouponApplyForm(data={'code': ' '})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('code' in form.errors)