from django.db import models

# Create your models here.


class UserProduct (models.Model):
    location = models.CharField(max_length=10)
