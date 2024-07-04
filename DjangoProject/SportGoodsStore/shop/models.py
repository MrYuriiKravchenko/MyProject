from django.db import models
from django.urls import reverse

from users.models import User


class Product(models.Model):
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE,
                                 verbose_name='категория')
    name = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='изображение')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    available = models.BooleanField(default=True, verbose_name='наличие')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создание')
    updated = models.DateTimeField(auto_now=True, verbose_name='изминение')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукт'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='категория')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='wishlists', on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, related_name='wishlists', on_delete=models.CASCADE, verbose_name='Продукт')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Список желаний'
        verbose_name_plural = 'Список желаний'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.user} - {self.product}"


class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE, verbose_name='продукт')
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE, verbose_name='пользователь')
    score = models.PositiveSmallIntegerField(verbose_name='оценка')

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-score']
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
            models.Index(fields=['score']),
        ]

    def __str__(self):
        return f'{self.user} - {self.product} - {self.score}'


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE, verbose_name='продукт')
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, verbose_name='пользователь')
    text = models.CharField(max_length=700, verbose_name='комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        unique_together = ('product', 'user')
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'{self.user} - {self.product} - {self.text[:20]}'
