from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone

from homework.models import Assignments, Submissions
from course.models import Courses, Selections

# Create your views here.

# Unfinished
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

    name = request.POST.get('assignmentName')
    description = request.POST.get('description')
    if (name is None or description is None) :
        raise Http404('Invalid request')

    addTime = timezone.now()
    deadlineTime = request.POST.get('deadlineTime')
    assignment = Assignments.objects.create(course=course, name=name, description=description, addTime=addTime, deadlineTime=deadlineTime)
    return HttpResponseRedirect(reverse("homework:index", args=(course_id,)))

@login_required
def delete(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    if request.user.type == "student":
        raise Http404("Student can't delete an assignment.")
    if course.teacher.id != request.user.id:
        raise Http404("You can't delete assignments of others' course.")
    assignment_id = request.POST.get('id')
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
        try:
            submission = Submissions.objects.get(assignment_id=assignment_id, student_id=request.user.id)
        except Submissions.DoesNotExist:
            submission =  None
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
    new_content = request.POST.get('content')
    assignment = Assignments.objects.get(pk=assignment_id)
    assignment.description = new_content
    assignment.save()
    return HttpResponseRedirect(reverse("homework:detail", args=(course_id, assignment_id)))

@login_required
def submit(request, course_id, assignment_id):
    # A post request for students to insert/update the submission in the database
    if request.user.type != 'student':
        raise Http404("Only students of this course could sumbit the assignment.")
    student_id = request.user.id
    submission_content = request.POST.get('content')
    try:
        submission = Submissions.objects.get(assignment_id=assignment_id, student_id=student_id)
    except Submissions.DoesNotExist:
        submission = None
    try:
        if submission is None:
            # Insert the submission
            Submissions.objects.create(assignment_id=assignment_id, student_id=student_id, content=submission_content, submissionTime=timezone.now())
        else:
            # Update the submission
            submission.content=submission_content
            submission.save()
    except Exception:
        raise Http404('Submission doesn''t contain content!')
    return HttpResponseRedirect(reverse("homework:detail", args=(course_id, assignment_id)))

@login_required
def submission(request, course_id, assignment_id, submission_id):
    # Detail of the submission
    data = {
            "submission_id": submission_id,
            "assignment_id": assignment_id,
            "course_id": course_id,
            }
    submission = get_object_or_404(Submissions, pk=submission_id)
    if request.user.type == 'student':
        if submission.student.id != request.user.id:
            raise Http404("You cannot access other student's submission.")
    elif request.user.type == 'teacher':
        if submission.assignment.course.teacher.id != request.user.id:
            raise Http404("You cannot access other teacher's course submission.")
    data["assgignmentName"] = submission.assignment.name
    data["studentName"] = submission.student.name
    data["content"] = submission.content
    data["submissionTime"] = submission.submissionTime
    data["score"] = submission.score
    data["comments"] = submission.comments
    return HttpResponse(str(data))

@login_required
def score(request, course_id, assignment_id, submission_id):
    # A post request to add/update the score of the submission in the database
    if request.user.type != 'teacher':
        raise Http404("Only teacher could score the assignments.")
    try:
        submission = Submissions.objects.get(pk=submission_id)
    except Submissions.DoesNotExist:
        raise Http404("Submission does not exist.")
    if submission.assignment.course.teacher.id != request.user.id:
        raise Http404("The submission is not your couse submission. You cannot access it.")

    try:
        score = request.POST.get('score')
        score = int(score)
        if score < 0 or score > 100:
            raise Exception
    except Exception:
        raise Http404("The score is illegal! Please check again. Make sure score is an integer between 0 and 100.")
    submission.score = score
    submission.save()
    return HttpResponseRedirect(reverse("homework:submission", args=(course_id, assignment_id, submission_id)))
