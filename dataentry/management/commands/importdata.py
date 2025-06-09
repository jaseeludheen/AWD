from django.core.management.base import BaseCommand
from dataentry.models import Student
import csv


# proposed command - python manage.py importdata file_path
# path name    -   /Users/jaseel/Downloads/student_details.csv
class Command(BaseCommand):
    help = 'Import data from CSV file into the database'


    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing data to import' )

    def handle(self, *args, **kwargs):
        # logic 
        file_path = kwargs['file_path']
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

                Student.objects.create(**row)  #

        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))



