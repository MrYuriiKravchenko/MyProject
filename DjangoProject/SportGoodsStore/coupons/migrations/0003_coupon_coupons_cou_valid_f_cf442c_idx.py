# Generated by Django 5.0.6 on 2024-07-04 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_alter_coupon_options_alter_coupon_active_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='coupon',
            index=models.Index(fields=['valid_from', 'valid_to'], name='coupons_cou_valid_f_cf442c_idx'),
        ),
    ]
