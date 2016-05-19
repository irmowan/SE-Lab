from django.db import models
import sys
sys.path.append("..")
from user.models import *


# Create your models here.

class Assignments(models.Model):
    # TODO
    assignmentId = models.CharField(max_length=30,primary_key=True)
    courseId = models.ForeignKey(Users, on_delete=models.CASCADE)
    assignmentName = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    addTime = models.DateTimeField()
    deadlineTime = models.DateTimeField(null=True)

class Submissions(models.Model):
    # TODO
    submissionId = models.CharField(max_length=30,primary_key=True)
    assignmentId = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    SubmissionTime = models.DateTimeField()
    score = models.IntegerField()
    comments = models.CharField(max_length=200)

