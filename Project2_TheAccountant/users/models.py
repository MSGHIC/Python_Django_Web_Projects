from django.db import models

import datetime
# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
   # add additional fields in here
 
   USERNAME = ['username']
   REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
  
   
   #date_of_birth =  models.DateField(default=date.today)
   def __str__(self):
        return self.username
   