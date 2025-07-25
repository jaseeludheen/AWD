from django.core.management.base import BaseCommand, CommandError
from dataentry.models import Student      # import  one model at a time is not a good idea, so we will import the model dynamically.
from django.apps import apps     # all models across all apps in the project can be imported dynamically.
import csv


# proposed command - python manage.py importdata file_path

#proposed command - python manage.py import data <fil_path/file_name.csv> model_name       ==> smarter way to do it.

# path name    -   /Users/jaseel/Downloads/student_details.csv



class Command_student(BaseCommand):
    help = 'Import student data from CSV file into the database'

    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing student data to import')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Student.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Student data imported from CSV successfully!'))



"""


class Commandq(BaseCommand):
    help = 'Import data from CSV file into the database'


    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing data to import' )
        parser.add_argument('model_name', type=str, help='Name of the model to import data into')  # This is not used in the current implementation, but can be used for future enhancements.


    def handle(self, *args, **kwargs):
        # logic 
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()  


        model = None  # initialize model to None, so that we can check if the model is found or not later.
        #search for models across all apps in the project
        for app_config in apps.get_app_configs():    # this get app config will have the metadata of all the apps
            #try to search for the model in the app config
            try:
                model = apps.get_model(app_config.label, model_name) 
                break  # stop searching once the model is found
            except LookupError:    # if the model is not found in the app config, continue to the next app config
                continue    #model not found in this app , so continue to the next app config


        if not model:
            raise CommandError(f'Model "{model_name}" not found in any app.')
        


#        print(file_path)
        with open(file_path, 'r') as file:   # with 
            reader = csv.DictReader(file)    #  dict reader is the pyhton built-in module to read csv file. Return an iterator that generates dictionaries for each row in the CSV file.
            for row in reader:
#                print(row)

     #      this is correct , but this is not the best way to insert data into the database.

#                Student.objects.create(
#                    roll_number=row['roll_number'],
#                    name=row['name'],
#                    age=row['age']
#                )

#                Student.objects.create(**row)  # create only student model. this is the best way to insert data into the database. It will automatically map the column names in the CSV file to the model fields.
                model.objects.create(**row)  # dynamically create the model object and save it to the database. the model is in try block above, so it will not raise an error if the model is not found.


        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))







"""