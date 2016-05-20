from django.db import models
from user.models import Users


# Create your models here.

class Courses(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Selections(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    student = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("course", "student"),)

