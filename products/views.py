from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def product_list(request):
    """Список продуктов"""
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})

def product_create(request):
    """Создание продукта"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно создан!')
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Создать продукт',
        'button_text': 'Создать'
    })

def product_update(request, pk):
    """Редактирование продукта"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно обновлен!')
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Редактировать продукт',
        'button_text': 'Сохранить'
    })

def product_delete(request, pk):
    """Удаление продукта"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Продукт успешно удален!')
        return redirect('products:product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})