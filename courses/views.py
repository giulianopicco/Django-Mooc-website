from itertools import chain

from datatableview import Datatable, columns
from datatableview.views import DatatableView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.template.defaultfilters import date as _date

from . import forms
from . import models


def courses(request):
    courses = models.Course.objects.all().filter(published=True)
    # return HttpResponse(courses)
    return render(request, 'courses/course_list.html', {'courses': courses, 'email': 'info@us.com'})


class CourseDatatable(Datatable):
    """"Vista del datable de cliente"""
    # titulo = columns.TextColumn(source='titulo')
    # imagen = columns.DisplayColumn('Imagen', processor='get_image')
    # fecha_inicio = columns.DateColumn(source='fecha_inicio', processor='get_fecha_inicio')
    # fecha_fin = columns.DateColumn(source='fecha_fin', processor='get_fecha_inicio')
    title = columns.TextColumn(source='title')
    description = columns.TextColumn(source='description')
    published = columns.BooleanColumn(source='published')
    created_at = columns.TextColumn(source='created_at', processor='get_fecha_inicio')
    acciones = columns.DisplayColumn('Acciones', processor='get_acciones')

    class Meta:  # pylint: disable=too-few-public-methods
        """"Configuracion del datatable"""
        model = models.Course
        id = 'dt-course'
        structure_template = "datatableview/bootstrap_structure.html"
        page_length = 50
        columns = []

    @staticmethod
    def get_fecha_inicio(instance, view, *args, **kwargs):  # pylint: disable=unused-argument
        return _date(instance.created_at, 'd/m/Y H:i')
    #
    # @staticmethod
    # def get_fecha_fin(instance, view, *args, **kwargs):  # pylint: disable=unused-argument
    #     return _date(instance.fecha_fin, 'd/m/Y H:i')
    #
    # @staticmethod
    # def get_image(instance, view, *args, **kwargs):  # pylint: disable=unused-argument
    #     """Botone del datatable"""
    #     return '<img src="{}" alt="user" style="max-width: 120px; max-height: 120px;">'.format(instance.imagen.url)
    #
    @staticmethod
    def get_acciones(instance, view, *args, **kwargs):  # pylint: disable=unused-argument
        """Botone del datatable"""
        rid = int(instance.pk)
        #
        url = reverse('courses:detail', args=[rid])
        aac = '<a class="btn waves-effect waves-light btn-sm btn-secondary" href="{}">' \
            '<i class="fa fa-eye"></i></a>'.format(url)
        # url = reverse('anuncio.update', args=[rid])
        # aac += ' <a class="btn waves-effect waves-light btn-sm btn-secondary" href="{}"><i class="fa fa-pencil">' \
        #        '</i></a>'.format(url)
        # url = reverse('anuncio.delete', args=[rid])
        # aac += ' <a class="btn waves-effect waves-light btn-sm btn-secondary" href="{}"><i class="fa fa-trash">' \
        #        '</i></a>'.format(url)
        return aac


# class AnuncioListView(PermissionRequiredMixin, DatatableView):  # pylint: disable=too-many-ancestors
class CourseListView(DatatableView):  # pylint: disable=too-many-ancestors
    """"Vista del listado de anuncio"""
    model = models.Course
    template_name = "courses/course_list.html"
    context_object_name = "course"
    datatable_class = CourseDatatable
    # permission_required = 'anuncio.add_anuncio'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.request.user.groups.filter(name='Cliente').exists():
    #         queryset = queryset.filter(cliente=self.request.user.perfil.cliente)
    #     return queryset
    #
    # def get_datatable_class(self):
    #     if self.request.user.groups.filter(name='Cliente').exists():
    #         return AnuncioDatatable
    #     return AnuncioStaffDatatable


def course_detail(request, pk):
    # course = get_object_or_404(models.Course, pk=pk)
    # steps = sorted(chain(course.textstep_set.all(), course.quizstep_set.all()), key=lambda step: step.order)
    try:
        course = models.Course.objects.prefetch_related('textstep_set', 'quizstep_set', 'quizstep_set__question_set').get(pk=pk, published=True)
    except models.Course.DoesNotExist:
        raise Http404
    else:
        steps = sorted(chain(course.textstep_set.all(), course.quizstep_set.all()), key=lambda step: step.order)
        return render(request, 'courses/detail.html', {'course': course, 'steps': steps})


def course_create(request):
    form = forms.CourseForm()
    if request.method == 'POST':
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'courses/course_form.html', {'form': form})


def text_step_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.TextStep, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/step_text_detail.html', {'step': step})


def quiz_step_detail(request, course_pk, step_pk):
    # step = get_object_or_404(models.QuizStep, course_id=course_pk, pk=step_pk)
    try:
        step = models.QuizStep.objects.select_related('course').prefetch_related('question_set')\
            .get(course_id=course_pk, pk=step_pk, course__published=True)
    except models.QuizStep.DoesNotExist:
        raise Http404
    else:
        return render(request, 'courses/step_quiz_detail.html', {
            'step': step,
            'max_num_answers': range(models.Question.objects.annotate(num_answers=Count('answers')).aggregate(Max('num_answers')).get('num_answers__max')),
        })


@login_required
def quiz_create(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    form = forms.QuizForm()

    if request.method == 'POST':
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.add_message(request, messages.SUCCESS, 'Quiz addded!')
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form})


@login_required
def quiz_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(models.QuizStep, pk=quiz_pk, course_id=course_pk)
    form = forms.QuizForm(instance=quiz)
    if request.method == 'POST':
        form = forms.QuizForm(instance=quiz, data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, '{} updated'.format(form.cleaned_data['title']))
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form, 'quiz': quiz, 'course': quiz.course})


@login_required
def create_question(request, quiz_pk, question_type):
    quiz = get_object_or_404(models.QuizStep, pk=quiz_pk)
    if question_type == 'tf':
        form_class = forms.TrueFalseQuestionForm
    else:
        form_class = forms.MultipleChoiceQuestionForm
    form = form_class()
    answer_forms = forms.AnswerInlineFormSet(
        queryset=models.Answer.objects.none()
    )

    if request.method == 'POST':
        form = form_class(request.POST)
        answer_forms = forms.AnswerInlineFormSet(request.POST, queryset=models.Answer.objects.none())

        if form.is_valid() and answer_forms.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, 'Added question')
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/question_form.html', {
        'quiz': quiz,
        'form': form,
        'formset': answer_forms,
        'question_type': question_type
    })


@login_required
def edit_question(request, quiz_pk, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk, quiz_id=quiz_pk)

    if hasattr(question, 'truefalsequestion'):
        form_class = forms.TrueFalseQuestionForm
    else:
        form_class = forms.MultipleChoiceQuestionForm
    form = form_class(instance=question)
    answer_forms = forms.AnswerInlineFormSet(
        queryset=form.instance.answers.all(),
        prefix='answers'
    )
    if request.method == 'POST':
        form = form_class(request.POST, instance=question)
        answer_forms = forms.AnswerInlineFormSet(
            request.POST,
            queryset=form.instance.answers.all(),
            prefix='answers'
        )
        if form.is_valid() and answer_forms.is_valid():
            form.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            for answer_delete in answer_forms.deleted_objects:
                answer_delete.delete()
            messages.success(request, 'Updated question')
            return HttpResponseRedirect(question.quiz.get_absolute_url())
    return render(request, 'courses/question_form.html', {
        'form': form,
        'quiz': question.quiz,
        'formset': answer_forms,
        'question_type': 'tf' if hasattr(question, 'truefalsequestion') else 'mc'
    })


@login_required
def create_answer(request, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)
    # form = forms.AnswerForm
    formset = forms.AnswerFormSet(queryset=question.answers.all())
    if request.method == 'POST':
        formset = forms.AnswerFormSet(request.POST, queryset=question.answers.all())
        if formset.is_valid():
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, 'Answers Added')
            return HttpResponseRedirect(question.quiz.get_absolute_url())
    return render(request, 'courses/answer_form.html', {
        'formset': formset,
        'question': question
    })


def courses_by_teacher(request, teacher):
    # this is not efficient
    # teacher = models.User.objects.get(username=teacher)
    # courses = teacher.course_set.all()
    courses = models.Course.objects.filter(teacher__username=teacher).filter(published=True)
    return render(request, 'courses/course_by_teacher.html', {'courses': courses})


def search(request):
    q = request.GET['q']
    courses = models.Course.objects.filter(
        Q(title__icontains=q) | Q(description__icontains=q)).filter(published=True)
    return render(request, 'courses/course_by_teacher.html', {'courses': courses})