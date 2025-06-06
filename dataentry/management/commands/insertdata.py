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
            {'roll_number': '1010', 'name': 'Anna', 'age': 22},
            {'roll_number': '1011', 'name': 'Joseph', 'age': 21},
            {'roll_number': '1009', 'name': 'Marley Brown', 'age': 23},
            {'roll_number': '1006', 'name': 'Jaseel', 'age': 24},
        ]

        """

        for data in dataset:
#            print(data['name'])
            
            Student.objects.create(roll_number=data['roll_number'],
                                   name=data['name'],
                                   age=data['age'])
        # print success message
        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))

        """


        for data in dataset:

            roll_no = data['roll_number']
            existing_record = Student.objects.filter(roll_number=roll_no).exists()

            if not existing_record:
                Student.objects.create(roll_number=data['roll_number'],
                                   name=data['name'],
                                   age=data['age'])
                self.stdout.write(self.style.SUCCESS(f'Data inserted successfully for {data['name']}.'))
            else:
                self.stdout.write(self.style.WARNING(f'Student with roll number {roll_no} already exists!'))

