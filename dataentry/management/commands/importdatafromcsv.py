from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
from django.db import DataError
from dataentry.utils import check_csv_errors




# proposed command - python manage.py importdata file_path
# proposed command - python manage.py import data <file_path/file_name.csv> model_name       ==> smarter way to do it.




class Command(BaseCommand):
    help = 'Import data from CSV file into the database'


    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing data to import' )
        parser.add_argument('model_name', type=str, help='Name of the model to import data into')  # This is not used in the current implementation, but can be used for future enhancements.


    def handle(self, *args, **kwargs):

        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()  

        model = check_csv_errors(file_path, model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)  
            for row in reader:
                model.objects.create(**row)  
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))






