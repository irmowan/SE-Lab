from django.db import models

# Create your models here.

class Users(models.Model):
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    id = models.CharField(max_length=11,primary_key=True)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.name

