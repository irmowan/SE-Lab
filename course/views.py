from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request, course_id):
	return HttpResponse("This is the index page of course {}.".format(course_id))

