from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.

def index(request, course_id):
    return HttpResponse("This is the index page of homework of course {}.".format(course_id))

def new(request, course_id):
    return HttpResponse("A empty page for the teacher to input new assignment.")

def create(request, course_id):
    # A post request to insert the new assignment into the database
    return HttpResponseRedirect(reverse("homework:index", args=(course_id,)))

def delete(request, course_id):
    # A post request to delete the selected assignments from the database
    return HttpResponseRedirect(reverse("homework:index", args=(course_id,)))

def detail(request, course_id, assignment_id):
    return HttpResponse("This is the detail page of assignment {} of course {}.".format(assignment_id, course_id))

def update(request, course_id, assignment_id):
    # A post request to modify the assignment in the database
    return HttpResponseRedirect(reverse("homework:detail", args=(course_id, assignment_id)))

def submit(request, course_id, assignment_id):
    # A post request to insert/update the submission in the database
    return HttpResponseRedirect(reverse("homework:detail", args=(course_id, assignment_id)))

def submission(request, course_id, assignment_id, submission_id):
    return HttpResponse("This is the detail page of submission {} of assignment {} of course {}.".format(submission_id, assignment_id, course_id))

def score(request, course_id, assignment_id, submission_id):
    # A post request to add/update the score of the submission in the database
    return HttpResponseRedirect(reverse("homework:submission", args=(course_id, assignment_id, submission_id)))

