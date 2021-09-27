
from django.db import models

# Create your models here.
class brewery(models.Model):
    brewery_name = models.CharField(max_length=100)