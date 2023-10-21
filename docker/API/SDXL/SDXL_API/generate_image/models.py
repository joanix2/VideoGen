from django.db import models

# Create your models here.

class ImageModel(models.Model):
    name = models.CharField(max_length=100)
    image_file = models.ImageField(upload_to='images/')
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name