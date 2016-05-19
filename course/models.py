from django.db import models
import sys
sys.path.append("..")
from user.models import *


# Create your models here.

class Courses(models.Model):
    # TODO
    courseId = models.CharField(max_length=30,primary_key=True)
    courseName = models.CharField(max_length=30)
    teacherId = models.ForeignKey(Users, on_delete=models.CASCADE)

class CourseSelection(models.Model):
    # TODO
    courseId = models.ForeignKey(Courses, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Users, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("courseId", "studentId"),)


