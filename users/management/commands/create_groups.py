# users/management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Product


class Command(BaseCommand):
    help = 'Создает группы и назначает права'

    def handle(self, *args, **options):
        # Создаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует'))

        # Получаем права
        content_type = ContentType.objects.get_for_model(Product)

        # Право на отмену публикации
        unpublish_perm, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=content_type,
        )

        # Право на удаление
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        # Назначаем права группе
        moderator_group.permissions.add(unpublish_perm, delete_perm)
        moderator_group.save()

        self.stdout.write(self.style.SUCCESS('Права назначены группе "Модератор продуктов"'))

        # Выводим информацию
        self.stdout.write('\nПрава группы "Модератор продуктов":')
        for perm in moderator_group.permissions.all():
            self.stdout.write(f'  - {perm.name} ({perm.codename})')