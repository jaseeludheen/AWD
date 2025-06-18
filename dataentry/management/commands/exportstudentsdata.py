import csv 
from django.core.management.base import BaseCommand
from dataentry.models import Student
import datetime


#  proposed command - python manage.py exportdata 

"""
step 1: fetch the data from the database
step 2: define the CSV file name / path
step 3: open the csv file and write the data


"""

class Command(BaseCommand):
    help = 'Export student data to a CSV file'

    def handle(self, *args, **kwargs):

        # fetch the data from the database
        students = Student.objects.all()

        # generate the timestamp of current data and time
        timestamp = datetime.datetime.now().strftime("%I:%M:%S %p %d-%m-%Y")
        
        # define the CSV file name / path
        file_path = f'exported_student_data_{timestamp}.csv'
        # open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # write the CSV header
            writer.writerow(['Roll Number', 'Name', 'Age' ])

            # write data rows
            for student in students:
                writer.writerow([student.roll_number, student.name, student.age])

            self.stdout.write(self.style.SUCCESS('Data exported successfully!'))


        

