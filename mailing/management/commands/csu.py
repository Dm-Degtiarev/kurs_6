from django.core.management import BaseCommand
from mailing.models import User


# Команда создания суперюзера. Так как мы сделали вход по почте,
# при этом отменили по логину, который должен быть обязательно в методе созданию СЮ
class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@django.ru',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('0001qwerty1000')
        user.save()
