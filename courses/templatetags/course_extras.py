from django import template
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
import markdown2

from courses.models import Course

register = template.Library()


@register.simple_tag
def newest_course():
    """Gets the most recent course"""
    lastest = Course.objects.latest('created_at')
    lastestUrl = reverse('courses:detail', kwargs={'pk': lastest.pk})
    return mark_safe('<li><a href="{}">{}</a></li>'.format(lastestUrl, lastest.title))


# @register.sim-er(request, 'courses/_navigation.html', {'courses': courses}, content_type='application/xhtml+xml')

@register.inclusion_tag('courses/_navigation.html')
def nav_courses_list():
    courses = Course.objects.filter(published=True).values('id', 'title').order_by('-created_at')[:5]  #just shows the last five courses
    return {'courses': courses}


@register.filter('time_estimate')
def time_estimate(word_count):
    """ Estimates the time it will take to complete a step """
    # return round(word_count/20)
    return round(word_count/2)


@register.filter('time_estimate_quiz')
def time_estimate_quiz(question_count):
    """ Estimates the time it will take to complete a step """
    return question_count * 2


@register.filter('markdown2html')
def markdown2html(markdown_text):
    """ Converts markdown text to html """
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)
