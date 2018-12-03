from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses, name='courses'),
    path('<int:course_pk>/<int:step_pk>', views.step_detail, name='step'),
    path('<int:pk>/', views.course_detail, name='detail'),
]