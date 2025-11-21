from django.core.management.base import BaseCommand
from accounts.models import CustomUser
import os


class Command(BaseCommand):
    help = 'Crea un superusuario inicial si no existe'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@estudify.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123456')

        if not CustomUser.objects.filter(username=username).exists():
            CustomUser.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado exitosamente'))
        else:
            self.stdout.write(self.style.WARNING(f'El superusuario "{username}" ya existe'))
