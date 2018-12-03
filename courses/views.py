from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Course, Step



def courses(request):
    courses = Course.objects.all()
    output = '\n'.join([str(course) for course in courses])
    # return HttpResponse(courses)
    return render(request, 'courses/course_list.html', {'courses':courses})

def course_detail(request, pk):
    c = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/detail.html ', {'course':c,})

def step_detail(request, course_pk, step_pk):
    step = get_object_or_404(Step, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/step_detail.html', {'step':step})