from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('', views.courses, name='list'),
    path('', views.CourseListView.as_view(), name='list'),
    path('create', views.course_create, name='create'),
    path('<int:course_pk>/t<int:step_pk>', views.text_step_detail, name='step.text'),
    path('<int:course_pk>/q<int:step_pk>', views.quiz_step_detail, name='step.quiz'),
    path('<int:course_pk>/create_quiz', views.quiz_create, name='quiz.create'),
    path('<int:course_pk>/edit_quiz/<int:quiz_pk>', views.quiz_edit, name='quiz.edit'),
    path('by/<teacher>', views.courses_by_teacher, name='by_teacher'),
    # Search
    path('search', views.search, name='search'),

    path('<int:quiz_pk>/edit_question/<int:question_pk>', views.edit_question, name='question.edit'),
    path('<int:quiz_pk>/create_question/<str:question_type>', views.create_question, name='question.create'),
    # re_path(r'(?P<quiz_pk>\d+)/create_question/(?P<question_type>)mc|tf/$',
    #         views.create_question,
    #         name='question.create'),

    path('<int:pk>/', views.course_detail, name='detail'),
    # Answer
    path('<int:question_pk>/create_answer', views.create_answer, name='answer.create'),
]