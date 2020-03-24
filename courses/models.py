from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


class Course(models.Model):

    STATUS_CHOICES = (
        ('i', 'In Progress'),
        ('r', 'In Review'),
        ('p', 'Published'),
    )

    teacher = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='i')
    # We should refactor it later in its own model
    subject = models.CharField(default='', max_length=100)

    def __str__(self):
        return '{}'.format(self.title)

    def time_to_complete(self):
        from courses.templatetags.course_extras import time_estimate
        return '{} min.'.format(time_estimate(len(self.description.split())))


class Step(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ['order',]
    
    def __str__(self):
        return self.title


class TextStep(Step):
    content = models.TextField(blank=True, default='')

    def get_absolute_url(self):
        return reverse('courses:step.text', kwargs={
            'course_pk': self.course_id,
            'step_pk': self.id
        })


class QuizStep(Step):
    total_questions = models.IntegerField("Number of questions", default=1)
    times_taken = models.IntegerField(default=0, editable=False)

    def get_absolute_url(self):
        return reverse('courses:step.quiz', kwargs={
            'course_pk': self.course_id,
            'step_pk': self.id
        })

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'


class Question(models.Model):
    quiz = models.ForeignKey(QuizStep, on_delete=models.deletion.CASCADE)
    order = models.IntegerField(default=0)
    prompt = models.TextField()

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return 'Question <{}>'.format(self.prompt)

    def get_absolute_url(self):
        return self.quiz.get_absolute_url()


class MultipleChoiceQuestion(Question):
    shuffle_anwsers = models.BooleanField(default=False)


class TrueFalseQuestion(Question):
    pass


class Answer(models.Model):
    question = models.ForeignKey(Question, models.deletion.CASCADE, 'answers')
    order = models.IntegerField(default=0)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return 'Answer <{}>'.format(self.text)
