# products/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    # Существующие поля
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название продукта'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание продукта'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        help_text='Цена должна быть положительной'
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='В наличии'
    )

    # НОВЫЕ ПОЛЯ
    is_published = models.BooleanField(
        default=False,  # По умолчанию не опубликован
        verbose_name='Опубликован',
        help_text='Отметьте, если продукт опубликован'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
        null=True,  # Временно разрешаем null для существующих продуктов
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']

        # Кастомные права
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        return self.name