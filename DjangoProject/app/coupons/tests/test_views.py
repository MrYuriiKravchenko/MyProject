from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from coupons.models import Coupon


class CouponApplyViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.valid_coupon = Coupon.objects.create(
            code='SUMMER2024',
            valid_from=timezone.now() - timezone.timedelta(days=1),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            discount=10,
            active=True
        )
        self.invalid_coupon = Coupon.objects.create(
            code='WINTER2024',
            valid_from=timezone.now() - timezone.timedelta(days=10),
            valid_to=timezone.now() - timezone.timedelta(days=1),
            discount=15,
            active=True
        )
        self.url = reverse('coupons:apply')

    def test_valid_coupon(self):
        response = self.client.post(self.url, {'code': 'SUMMER2024'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['coupon_id'], self.valid_coupon.id)
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_invalid_coupon(self):
        response = self.client.post(self.url, {'code': 'WINTER2024'})
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.client.session.get('coupon_id'))
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_non_existent_coupon(self):
        response = self.client.post(self.url, {'code': 'NONEXISTENT'})
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.client.session.get('coupon_id'))
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_empty_code(self):
        response = self.client.post(self.url, {'code': ''})
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.client.session.get('coupon_id'))
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_inactive_coupon(self):
        inactive_coupon = Coupon.objects.create(
            code='INACTIVE2024',
            valid_from=timezone.now() - timezone.timedelta(days=1),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            discount=10,
            active=False
        )
        response = self.client.post(self.url, {'code': 'INACTIVE2024'})
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.client.session.get('coupon_id'))
        self.assertRedirects(response, reverse('cart:cart_detail'))
