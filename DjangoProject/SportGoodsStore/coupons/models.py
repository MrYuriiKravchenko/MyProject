from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='код')
    valid_from = models.DateTimeField(verbose_name='начинает дествовать с')
    valid_to = models.DateTimeField(verbose_name='действителен до')
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)],
        help_text='Процент скидки (от 0 до 100)')
    active = models.BooleanField(verbose_name='активен')

    class Meta:
        verbose_name = 'Купоны'
        verbose_name_plural = 'Купоны'
        indexes = [
            models.Index(fields=['valid_from', 'valid_to']),
        ]

    def __str__(self):
        return self.code
