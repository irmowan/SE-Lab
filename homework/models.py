from django.db import models
from user.models import Users
from course.models import Courses


# Create your models here.

class Assignments(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()
    addTime = models.DateTimeField()
    deadlineTime = models.DateTimeField(null=True)

class Submissions(models.Model):
    assignmentId = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    submissionTime = models.DateTimeField()
    score = models.IntegerField()
    comments = models.TextField()
