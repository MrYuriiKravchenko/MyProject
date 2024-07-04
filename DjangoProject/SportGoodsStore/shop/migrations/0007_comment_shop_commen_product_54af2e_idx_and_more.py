# Generated by Django 5.0.6 on 2024-07-04 11:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_comment_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['product'], name='shop_commen_product_54af2e_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['user'], name='shop_commen_user_id_1e7887_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['created'], name='shop_commen_created_d90939_idx'),
        ),
        migrations.AddIndex(
            model_name='rating',
            index=models.Index(fields=['product'], name='shop_rating_product_5351ea_idx'),
        ),
        migrations.AddIndex(
            model_name='rating',
            index=models.Index(fields=['user'], name='shop_rating_user_id_0054b8_idx'),
        ),
        migrations.AddIndex(
            model_name='rating',
            index=models.Index(fields=['score'], name='shop_rating_score_b50420_idx'),
        ),
        migrations.AddIndex(
            model_name='wishlist',
            index=models.Index(fields=['user'], name='shop_wishli_user_id_1c58f1_idx'),
        ),
        migrations.AddIndex(
            model_name='wishlist',
            index=models.Index(fields=['product'], name='shop_wishli_product_40cef0_idx'),
        ),
    ]