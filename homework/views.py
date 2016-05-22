from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from homework.models import Assignments, Submissions
import datetime
# Create your views here.

def index(request, course_id):
    return HttpResponse("This is the index page of homework of course {}.".format(course_id))

def new(request, course_id):
    return HttpResponse("A empty page for the teacher to input new assignment.")

def create(request, course_id):
    # A post request to insert the new assignment into the database
    # get message from Httprequest
    assignment_name = request.post['assignmentname']
    assignment_description = request.post['description']
    assignment_addTime = datetime.now()
    assignment_deadlineTime = request.post['deadlineTime']
    assignment = Assignments(course = course_id,name = assignment_name,description = assignment_description,addTime = assignment_addTime,deadlineTime = assignment_deadlineTime)
    assignment.save()
    return HttpResponseRedirect(reverse("homework:index", args=(course_id,)))

def delete(request, course_id):
    # A post request to delete the selected assignments from the database
    # get assignment_id from Httprequest
    assignment_id = request.post['delete_assignment_id']
    if Assignments.objects.get(pk=assignment_id)!=null:
        Assignments.objects.get(pk=assignment_id).delete()
    return HttpResponseRedirect(reverse("homework:index", args=(course_id,)))

def detail(request, course_id, assignment_id):
    return HttpResponse("This is the detail page of assignment {} of course {}.".format(assignment_id, course_id))

def update(request, course_id, assignment_id):
    # A post request to modify the assignment in the database
    if request.user.type != 'teacher':
        raise Http404("Only the teacher of the course could modify the assignemnt.")
    new_content = request.post['content']
    assignment = Assignments.objects.get(pk=assignment_id)
    assignment.update(description=new_content)
    assignment.save()
    return HttpResponseRedirect(reverse("homework:detail", args=(course_id, assignment_id)))

def submit(request, course_id, assignment_id):
    # A post request to insert/update the submission in the database
    if request.user.type != 'student':
        raise Http404("Only students of this course could sumbit the assignment.")
    student_id = request.post['student_id']
    submission_content = request.post['content']
    if Assignments.objects.get(assignmentId=assignment_id, studentId=student_id) != null:
        # Insert the submission
        course_id = Assignments.objects.get(pk=assignment_id).course
        submit_time = datetime.now()
        submission = Submissions(assignmentId=assignment_id, studentId=student_id, content=submission_content, submissionTime=submit_time)
        submission.save()
    else:
        # Update the submission
        submission = Assignments.objects.get(assignmentId=assignment_id, studentId=student_id)
        submission.update(content=submission_content)
        submission.save()
    return HttpResponseRedirect(reverse("homework:detail", args=(course_id, assignment_id)))

def submission(request, course_id, assignment_id, submission_id):
    # Detail of the submission
    if request.user.type != 'teacher':
        raise Http404("You cannot access the details of al")
    submission = Submissions.objects.get(pk=submission_id)
    assignment_id = submission.assignmentId
    assignment = Assignments.objects.get(pk=submission.assignmentId)
    course_id = assignment.course
    return HttpResponse("This is the detail page of submission {} of assignment {} of course {}.".format(submission_id, assignment_id, course_id))

def score(request, course_id, assignment_id, submission_id):
    # A post request to add/update the score of the submission in the database
    if request.user.type != 'teacher':
        raise Http404("Only teacher could score the assignments.")
    student_id = request.post['student_id']
    score = request.post['score']
    if score < 0 or score > 100:
        raise Http404("The score is illegal! Please check again.")
    submission = Submissions.objects.get(pk=submission_id)
    submission.update(score=score)
    submission.save()
    return HttpResponseRedirect(reverse("homework:submission", args=(course_id, assignment_id, submission_id)))
