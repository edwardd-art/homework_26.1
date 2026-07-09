# products/forms.py

from django import forms
from .models import Product

# Список запрещенных слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'is_available']
        # Убираем is_published и owner - они будут заполняться автоматически

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название продукта',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание продукта',
            'rows': 4,
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите цену',
            'step': '0.01',
            'min': '0',
        })
        self.fields['is_available'].widget.attrs.update({
            'class': 'form-check-input',
        })

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for forbidden_word in FORBIDDEN_WORDS:
                if forbidden_word in name_lower:
                    raise forms.ValidationError(
                        f'Название содержит запрещенное слово: "{forbidden_word}"'
                    )
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            description_lower = description.lower()
            for forbidden_word in FORBIDDEN_WORDS:
                if forbidden_word in description_lower:
                    raise forms.ValidationError(
                        f'Описание содержит запрещенное слово: "{forbidden_word}"'
                    )
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена продукта не может быть отрицательной.')
        return price