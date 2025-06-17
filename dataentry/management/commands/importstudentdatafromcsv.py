from django.core.management.base import BaseCommand
from dataentry.models import Student
import csv
 
# importstudentdatafromcsv.py
# Command to import student data from a CSV file into the database

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
