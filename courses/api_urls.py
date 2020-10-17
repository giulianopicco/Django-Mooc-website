from django.urls import path, re_path
from . import views
from . import viewset

urlpatterns = [
    # REST framework
    path('', viewset.ListCreateCourseGenerics.as_view(), name='course_list'),
    path('<int:pk>', viewset.RetrieveUpdateDestroyCourse.as_view(), name='course_detail'),
    path('<int:course_pk>/reviews', viewset.ListCreateReview.as_view(), name='review_list'),
    path('<int:course_pk>/reviews/<int:pk>', viewset.RetrieveUpdateDestroyReview.as_view(), name='review_detail')
]