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

    def __str__(self):
        return self.name

class Submissions(models.Model):
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    student = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    submissionTime = models.DateTimeField()
    score = models.IntegerField(null=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return str(self.assignment) + ": " + str(self.student)

