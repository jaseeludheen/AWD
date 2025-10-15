from django.db import models
from django.contrib.auth.models import User



class CompressImage(models.Model):
    # [(10, 10), (20, 20), (30, 30) ..., (100, 100)]   (value, label)
    QUALITY_CHOICES = [(i, f"{i}%") for i in range(10, 101, 10)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='original_images/')
    quality = models.IntegerField(choices=QUALITY_CHOICES, default=80)
    compressed_image = models.ImageField(upload_to='compressed_images/')
    compressed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    