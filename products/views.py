# products/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    """Список всех продуктов (доступен всем)"""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']

    def get_queryset(self):
        # Показываем только опубликованные продукты
        return Product.objects.filter(is_published=True).order_by('-created_at')


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class ProductCreateView(CreateView):
    """Создание продукта (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        # Автоматически назначаем владельца
        form.instance.owner = self.request.user
        # По умолчанию продукт не опубликован
        form.instance.is_published = False
        messages.success(self.request, 'Продукт создан и отправлен на модерацию!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать продукт'
        context['button_text'] = 'Создать'
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта (только владелец или модератор)"""
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')
    login_url = 'users:login'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        # Проверяем права
        if obj.owner == user or user.has_perm('products.can_unpublish_product'):
            return obj
        else:
            raise PermissionDenied('У вас нет прав на редактирование этого продукта')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать продукт'
        context['button_text'] = 'Сохранить'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно обновлен!')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта (владелец или модератор)"""
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')
    login_url = 'users:login'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        # Проверяем права: владелец ИЛИ модератор (имеет право на удаление)
        if obj.owner == user or user.has_perm('products.delete_product'):
            return obj
        else:
            raise PermissionDenied('У вас нет прав на удаление этого продукта')


@login_required
@permission_required('products.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    """Отмена публикации продукта (только для модераторов)"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_published = False
        product.save()
        messages.success(request, f'Продукт "{product.name}" снят с публикации')
        return redirect('products:product_list')

    return render(request, 'products/unpublish_confirm.html', {'product': product})


@login_required
def publish_product(request, pk):
    """Публикация продукта (для владельца или модератора)"""
    product = get_object_or_404(Product, pk=pk)
    user = request.user

    # Проверяем права
    if product.owner == user or user.has_perm('products.can_unpublish_product'):
        product.is_published = True
        product.save()
        messages.success(request, f'Продукт "{product.name}" опубликован')
    else:
        messages.error(request, 'У вас нет прав на публикацию этого продукта')

    return redirect('products:product_list')