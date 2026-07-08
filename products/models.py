from django.db import models


class Product(models.Model):
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
        verbose_name='В наличии',
        help_text='Отметьте, если продукт есть в наличии'
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

    def __str__(self):
        return self.name