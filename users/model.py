from django.db import models
from django.db.models.enums import Choices
from django.forms import ModelForm

class user(models.Model):
    username = None
    first_name= models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password1 = models.CharField(max_length = 12)
    password = models.CharField(max_length = 12)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        return self.email