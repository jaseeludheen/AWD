from django.db import models

# Create your models here.



class Upload(models.Model):    # file path will be storing in the database.
    file = models.FileField(upload_to='uploads/')   # upload_to  ==> means the file will be uploaded to MEDIA_ROOT/uploads/
    model_name = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # auto_now_add will set the current date and time when the object is created

    def __str__(self):
        return self.model_name