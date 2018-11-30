from django.shortcuts import render
from django.http import HttpResponse

from .models import Course



def courses(request):
    courses = Course.objects.all()
    output = '\n'.join([str(course) for course in courses])
    # return HttpResponse(courses)
    return render(request, 'courses/course_list.html', {'courses':courses})