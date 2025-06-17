from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
import re  # Regular expression for employee ID validation

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


        model = None  
        for app_config in apps.get_app_configs():    
            try:
                model = apps.get_model(app_config.label, model_name) 
                break  
            except LookupError:    
                continue   


        if not model:
            raise CommandError(f'Model "{model_name}" not found in any app.')
        

        with open(file_path, 'r') as file:  
            reader = csv.DictReader(file)  
            for row in reader:
                # Check employee_id for Employee model
                if model_name == 'Employee':
                    employee_id = row.get('employee_id', '')
                    if not re.match(r'^EMP\d{4}$', employee_id):
                        self.stdout.write(f'Skipping bad ID: {employee_id}')
                        continue
                    if model.objects.filter(employee_id=employee_id).exists():
                        self.stdout.write(f'Skipping duplicate ID: {employee_id}')
                        continue
                model.objects.create(**row)                 
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))






