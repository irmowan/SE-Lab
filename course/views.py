from django.shortcuts import render
from django.http import HttpResponse, Http404
from course.models import Courses, Selections
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required
def index(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    data = {'name': course.name}
    if request.user.type == "teacher":
        if course.teacher.id != request.user.id:
            raise Http404("You can't access others' course.")
        data['count'] = course.selections_set.count()
    else:
        if not Selections.objects.filter(course_id=course_id, student_id=request.user.id):
            raise Http404("You have not selected the course.")
        data['teacherName'] = course.teacher.name
    return HttpResponse(str(data))
