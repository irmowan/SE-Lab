from django.shortcuts import render
from django.http import HttpResponse
from course.models import Courses

# Create your views here.

def index(request, course_id):
    course = Courses.objects.get(pk=course_id)
    response = "Name: {} <br/> Teacher: {} <br/> Number of students: {}".format(course.name, course.teacher.name, course.selections_set.count())
    return HttpResponse(response)

