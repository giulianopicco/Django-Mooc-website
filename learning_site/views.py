from django.db.models import Count
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from courses.models import Course
from . import forms


def hello(request):
    # latest_courses = list(Course.objects.all().order_by('created_at').filter(published=True))[-5:]
    latest_courses = list(Course.objects.all().order_by('created_at'
                                                        ).filter(published=True
                                                        ).annotate(total_steps=Count('textstep', distinct=True) + Count('quizstep', distinct=True)))[-15:]
    return render(request, 'home.html', {'latest_courses': latest_courses})


def suggestion_view(request):
    form = forms.SuggestionForm()
    if request.method == 'POST':
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            send_mail(
                'suggestion from {}'.format(form.cleaned_data['name']),
                form.cleaned_data['suggestion'],
                '{name} <{email}>'.format(**form.cleaned_data),
                ['giulianopicco@gmail.com']
            )
            messages.add_message(request, messages.SUCCESS, 'Thanks for your suggestion')
            return HttpResponseRedirect(reverse('suggestions'))
    return render(request, 'sugestion_form.html', {'form': form, 'courses':Course.objects.all})
