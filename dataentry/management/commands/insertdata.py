from django.core.management.base import BaseCommand
from dataentry.models import Student


# add some data to the database using the custom command

class Command(BaseCommand):

    help = 'Insert data into the database'

    def handle(self, *args, **kwargs):

        # add 1 data
#        Student.objects.create(roll_number='1001', name='John Doe', age=20)

        # add multiple data
        dataset = [
            {'roll_number': '1002', 'name': 'Alice Smith', 'age': 22},
            {'roll_number': '1003', 'name': 'Bob Johnson', 'age': 21},
            {'roll_number': '1004', 'name': 'Charlie Brown', 'age': 23},
            {'roll_number': '1005', 'name': 'Diana Prince', 'age': 24},
        ]
        for data in dataset:
#            print(data['name'])
            
            Student.objects.create(roll_number=data['roll_number'],
                                   name=data['name'],
                                   age=data['age'])
        # print success message
        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))


