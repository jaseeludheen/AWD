from django.core.management.base import BaseCommand
from django.apps import apps
import csv
import re # Regular expression for employee ID validation

class Command(BaseCommand):
    help = 'Import CSV data'

    def add_arguments(self, parser):
        parser.add_argument('file_path', help='CSV file path')
        parser.add_argument('model_name', help='Model name')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        # Get model
        try:
            model = apps.get_model('dataentry', model_name)
        except:
            self.stdout.write(f'Model {model_name} not found.')
            return

        # Read CSV
        try:
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
            self.stdout.write('Data imported!')
        except FileNotFoundError:
            self.stdout.write(f'File {file_path} not found.')