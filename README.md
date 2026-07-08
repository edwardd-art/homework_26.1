# Управление продуктами - Django CRUD

## Описание
Веб-приложение на Django для управления продуктами с полным CRUD функционалом.

## Функциональность
- ✅ Создание продуктов
- ✅ Просмотр списка продуктов  
- ✅ Редактирование продуктов
- ✅ Удаление продуктов
- ✅ Валидация запрещенных слов
- ✅ Валидация цены
- ✅ Стилизованные формы

## Запрещенные слова
При создании продукта проверяются:
- казино, криптовалюта, крипта, биржа
- дешево, бесплатно, обман, полиция, радар

## Установка

```bash
# Клонирование
git clone <url-репозитория>
cd my_django_project

# Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Зависимости
pip install -r requirements.txt

# Миграции
python manage.py makemigrations
python manage.py migrate

# Создание админа
python manage.py createsuperuser

# Запуск
python manage.py runservergit add README.md
