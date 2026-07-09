# products/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.core.cache import cache
from .models import Product
from .forms import ProductForm
from .services import ProductService


class ProductListView(ListView):
    """Список всех продуктов (доступен всем)"""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        # Используем кешированный список
        return ProductService.get_all_products_cached()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем список категорий для навигации
        context['categories'] = ProductService.get_categories_list()
        return context


class ProductDetailView(DetailView):
    """Детальная страница продукта (с кешированием)"""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # Используем сервис с кешированием
        product_id = self.kwargs.get('pk')
        product = ProductService.get_product_detail(product_id)

        if product is None:
            raise PermissionDenied('Продукт не найден или не опубликован')

        return product


class ProductCategoryView(ListView):
    """Список продуктов по категории (с кешированием)"""
    model = Product
    template_name = 'products/product_category.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category = self.kwargs.get('category')
        return ProductService.get_products_by_category(category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        context['categories'] = ProductService.get_categories_list()
        return context


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class ProductCreateView(CreateView):
    """Создание продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = False
        response = super().form_valid(form)

        # Очищаем кеш после создания
        ProductService.clear_product_cache(category_id=form.instance.category)
        cache.delete('products_all')

        messages.success(self.request, 'Продукт создан и отправлен на модерацию!')
        return response


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class ProductUpdateView(UpdateView):
    """Редактирование продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if obj.owner == user or user.has_perm('products.can_unpublish_product'):
            return obj
        else:
            raise PermissionDenied('У вас нет прав на редактирование этого продукта')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Очищаем кеш после обновления
        ProductService.clear_product_cache(
            product_id=self.object.id,
            category_id=self.object.category
        )
        cache.delete('products_all')

        messages.success(self.request, 'Продукт успешно обновлен!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать продукт'
        context['button_text'] = 'Сохранить'
        return context


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class ProductDeleteView(DeleteView):
    """Удаление продукта"""
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if obj.owner == user or user.has_perm('products.delete_product'):
            return obj
        else:
            raise PermissionDenied('У вас нет прав на удаление этого продукта')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        category = product.category

        # Очищаем кеш перед удалением
        ProductService.clear_product_cache(
            product_id=product.id,
            category_id=category
        )
        cache.delete('products_all')

        messages.success(request, 'Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)


@login_required
@permission_required('products.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    """Отмена публикации продукта"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_published = False
        product.save()

        # Очищаем кеш
        ProductService.clear_product_cache(
            product_id=product.id,
            category_id=product.category
        )
        cache.delete('products_all')

        messages.success(request, f'Продукт "{product.name}" снят с публикации')
        return redirect('products:product_list')

    return render(request, 'products/unpublish_confirm.html', {'product': product})


@login_required
def publish_product(request, pk):
    """Публикация продукта"""
    product = get_object_or_404(Product, pk=pk)
    user = request.user

    if product.owner == user or user.has_perm('products.can_unpublish_product'):
        product.is_published = True
        product.save()

        # Очищаем кеш
        ProductService.clear_product_cache(
            product_id=product.id,
            category_id=product.category
        )
        cache.delete('products_all')

        messages.success(request, f'Продукт "{product.name}" опубликован')
    else:
        messages.error(request, 'У вас нет прав на публикацию этого продукта')

    return redirect('products:product_list')