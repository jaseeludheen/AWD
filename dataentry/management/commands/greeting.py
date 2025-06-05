
from django.core.management.base import BaseCommand


# proposed command =  python manage.py greeting John

# proposed output = Hi {name} , Good morninig


class Command(BaseCommand):
    help = 'Greets the user with a friendly message'   # commad level help text.


    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Specifies user name')    # help - argument level help text. 



    def handle(self, *args, **kwargs):

        name = kwargs['name']  # get the name from the command line argument
        greeting = f'Hi {name}, Good morning!'  # create the greeting message
        self.stdout.write(greeting)  # print the greeting message to the console
        self.stderr.write(greeting)  # print the greeting message to the console as an error (optional, for demonstration) , color will be red in the terminal

        self.stdout.write(self.style.SUCCESS(greeting))  # print the greeting message to the console as a success message (optional, for demonstration), color will be green in the terminal
        self.stdout.write(self.style.WARNING(greeting))  # Yellow color
