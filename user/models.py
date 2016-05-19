from django.db import models

# Create your models here.

class Users(models.Model):
    # TODO
    userId = models.CharField(max_length=11,primary_key=True)
    userName = models.CharField(max_length=30)
    userType = models.DateTimeField('date published')


