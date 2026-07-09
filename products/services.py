# products/services.py

from django.core.cache import cache
from django.db.models import Q
from .models import Product
from django.conf import settings


class ProductService:
    """Сервис для работы с продуктами с кешированием"""

    @staticmethod
    def get_products_by_category(category_id, use_cache=True):
        """
        Получить все продукты в указанной категории.
        Использует кеширование для оптимизации.
        """
        cache_key = f'category_{category_id}'

        if use_cache:
            # Пытаемся получить данные из кеша
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data

        # Получаем продукты по категории
        products = Product.objects.filter(
            category=category_id,
            is_published=True
        ).select_related('owner').order_by('-created_at')

        # Сохраняем в кеш
        if use_cache:
            cache.set(
                cache_key,
                products,
                timeout=settings.CACHE_TTL
            )

        return products

    @staticmethod
    def get_product_detail(product_id, use_cache=True):
        """
        Получить детальную информацию о продукте.
        Использует кеширование.
        """
        cache_key = f'product_{product_id}'

        if use_cache:
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data

        try:
            product = Product.objects.select_related('owner').get(
                id=product_id,
                is_published=True
            )
            cache.set(cache_key, product, timeout=settings.CACHE_TTL)
            return product
        except Product.DoesNotExist:
            return None

    @staticmethod
    def clear_product_cache(product_id=None, category_id=None):
        """Очистить кеш продукта или категории"""
        if product_id:
            cache.delete(f'product_{product_id}')
        if category_id:
            cache.delete(f'category_{category_id}')
        # Также очищаем общий кеш списка
        cache.delete('products_all')

    @staticmethod
    def get_all_products_cached():
        """Получить все опубликованные продукты с кешем"""
        cache_key = 'products_all'
        products = cache.get(cache_key)

        if products is None:
            products = Product.objects.filter(
                is_published=True
            ).select_related('owner').order_by('-created_at')
            cache.set(cache_key, products, timeout=settings.CACHE_TTL)

        return products

    @staticmethod
    def get_categories_list():
        """Получить список всех категорий с кешем"""
        cache_key = 'categories_list'
        categories = cache.get(cache_key)

        if categories is None:
            categories = Product.objects.filter(
                is_published=True
            ).values_list('category', flat=True).distinct().exclude(
                category__isnull=True
            ).exclude(category='')
            cache.set(cache_key, list(categories), timeout=settings.CACHE_TTL * 2)

        return categories