from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)],
        help_text='Процент скидки (от 0 до 100)')
    active = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(fields=['valid_from', 'valid_to']),
        ]

    def __str__(self):
        return self.code
