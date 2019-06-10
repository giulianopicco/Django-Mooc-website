from datetime import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Course, Step


class CourseModelTests(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Python Regular Expressions',
            description="Learn to write regular expression in Python",
            created_at=timezone.now()
        )

    def test_course_creation(self):
        now = timezone.now()
        self.assertLessEqual(self.course.created_at, now)


class StepModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Python Regular Expressions',
            description="Learn to write regular expression in Python",
            created_at=timezone.now()
        )

    def test_step_creation(self):
        step = Step.objects.create(
            title='First Step',
            description='Instruction for your first step',
            content='Make sure to make your first step',
            order=1,
            course=self.course
        )

        self.assertIn(step, self.course.step_set.all())


class CourseViewsTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Python Testing',
            description='Learn to write test in Python'
        )
        self.course2 = Course.objects.create(
            title='New course',
            description='A new course'
        )
        self.step = Step.objects.create(
            title='Introduction to Doctest',
            description='Learn to write test in your docstring',
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])
        self.assertTemplateUsed(resp, 'courses/detail.html')
        self.assertContains(resp, self.course.title)

    def test_course_step_view(self):
        resp = self.client.get(reverse('courses:step',
                                       kwargs={'course_pk': self.course.pk,
                                               'step_pk': self.step.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])
        self.assertTemplateUsed(resp, 'courses/step_detail.html')
        self.assertContains(resp, self.step.title)
