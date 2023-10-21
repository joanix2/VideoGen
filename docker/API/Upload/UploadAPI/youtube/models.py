from django.db import models

# Create your models here.
class GoogleAPISecrets(models.Model):
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)