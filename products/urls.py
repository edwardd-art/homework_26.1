# products/urls.py

from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCategoryView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    unpublish_product,
    publish_product
)

app_name = 'products'

urlpatterns = [
    # Главная и список
    path('', ProductListView.as_view(), name='product_list'),

    # Категории
    path('category/<str:category>/', ProductCategoryView.as_view(), name='product_category'),

    # Детальная страница
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # CRUD
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Публикация
    path('<int:pk>/unpublish/', unpublish_product, name='unpublish'),
    path('<int:pk>/publish/', publish_product, name='publish'),
]