# products/models.py

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    # Существующие поля
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
        null=True,
        blank=True
    )

    # НОВОЕ ПОЛЕ: Категория
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Категория',
        help_text='Например: электроника, одежда, книги и т.д.'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        return self.name