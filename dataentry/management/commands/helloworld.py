from django.core.management.base import BaseCommand


class Command(BaseCommand):     #   $ python manage.py helloworld --help
    help = 'Prints Hello World'

    def handle(self, *args, **kwargs):
        # it's static
        self.stdout.write('Hello World')
        self.stdout.write('This is a custom management command in Django.')
        self.stdout.write('You can run this command using: python manage.py helloworld')