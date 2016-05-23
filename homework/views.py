from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import datetime

from homework.models import Assignments, Submissions
from course.models import Courses, Selections

# Create your views here.

@login_required
def index(request, course_id):
    return HttpResponse("This is the index page of homework of course {}.".format(course_id))

@login_required
def new(request, course_id):
    if request.user.type == "student":
        raise Http404("Student can't create an assignment.")
    return HttpResponse("A empty page for the teacher to input new assignment.")

@login_required
def create(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    if request.user.type == "student":
        raise Http404("Student can't create an assignment.")
    if course.teacher.id != request.user.id:
        raise Http404("You can't create assignments of others' course.")

    name = request.POST['assignmentName']
    description = request.POST['description']
    addTime = datetime.now()
    deadlineTime = request.POST['deadlineTime']
    assignment = Assignments.objects.create(course=course, name=name, description=description, addTime=addTime, deadlineTime=deadlineTime)
    return HttpResponseRedirect(reverse("homework:index", args=(course_id,)))

@login_required
def delete(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    if request.user.type == "student":
        raise Http404("Student can't delete an assignment.")
    if course.teacher.id != request.user.id:
        raise Http404("You can't delete assignments of others' course.")

    assignment_id = request.POST['id']
    assignment = get_object_or_404(Assignments, pk=assignment_id)
    assignment.delete()
    return HttpResponseRedirect(reverse("homework:index", args=(course_id,)))

@login_required
def detail(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignments, pk=assignment_id)
    if assignment.course.id != int(course_id):
        raise Http404("The assignent doesn't belong to the course.")
    data = {
        "assignmentName": assignment.name,
        "courseName": assignment.course.name,
        "teacherName": assignment.course.teacher.name,
        "description": assignment.description,
        "addTime": assignment.addTime,
        "deadlineTime": assignment.deadlineTime,
    }
    if request.user.type == "student":
        if not Selections.objects.filter(course_id=course_id, student_id=request.user.id):
            raise Http404("You have not selected the course.")
        submission = Submissions.objects.get(assignment_id=assignment_id, student_id=request.user.id)
        if submission is None:
            data["submissionStatus"] = False
        else:
            data["submissionStatus"] = True
            data["content"] = submission.content
            data["submissionTime"] = submission.submissionTime
            data["score"] = submission.score
            data["comments"] = submission.comments
    else:
        if assignment.course.teacher.id != request.user.id:
            raise Http404("You can't access assignments of others' course.")
        submissions = Submissions.objects.filter(assignment_id=assignment_id)
        data["submissions"] = [{"name": x.student.name, "score": x.score} for x in submissions]
    return HttpResponse(str(data))

@login_required
def update(request, course_id, assignment_id):
    # A post request to modify the assignment in the database
    if request.user.type != 'teacher':
        raise Http404("Only the teacher of the course could modify the assignment.")
    new_content = request.post['content']
    assignment = Assignments.objects.get(pk=assignment_id)
    assignment.update(description=new_content)
    assignment.save()
    return HttpResponseRedirect(reverse("homework:detail", args=(course_id, assignment_id)))

@login_required
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

@login_required
def submission(request, course_id, assignment_id, submission_id):
    # Detail of the submission
    if request.user.type != 'teacher':
        raise Http404("You cannot access the details of al")
    submission = Submissions.objects.get(pk=submission_id)
    assignment_id = submission.assignmentId
    assignment = Assignments.objects.get(pk=submission.assignmentId)
    course_id = assignment.course
    return HttpResponse("This is the detail page of submission {} of assignment {} of course {}.".format(submission_id, assignment_id, course_id))

@login_required
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
