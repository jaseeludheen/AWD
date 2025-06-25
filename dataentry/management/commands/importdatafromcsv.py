from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
from django.db import DataError


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
        
        # compare csv header with model's field names
        
        # Get the field names from the model that we found
#       model_fields = [field.name for field in model._meta.fields]    # id field is also included in the model fields, so we can use it to compare with the csv header
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']    # excluding the id field
        model_fields_set = set([field.strip().lower() for field in model_fields])

#       print(model_fields_set)


        with open(file_path, 'r') as file:  
            reader = csv.DictReader(file)  #  first row of the CSV file is considered as the header
            # fetch the header from the csv file
            csv_header = reader.fieldnames     # header of the csv file
            csv_fields = set([field.strip().lower() for field in csv_header])  # strip() removes spaces like " Name " ➜ "Name".      lower() makes it lowercase, so "Name" ➜ "name". and  convert it to a set to allow unordered comparison.

            # compare csv header with model's field names
            """
            if csv_fields != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields.")
            """
            # Compare sets (case-insensitive, order-insensitive)
            if not model_fields_set.issubset(csv_fields):
                raise DataError(f"CSV file headers do not match the fields of the {model_name} model.\nExpected fields: {model_fields}\nCSV headers: {csv_header}")


            for row in reader:
                model.objects.create(**row)  
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))






