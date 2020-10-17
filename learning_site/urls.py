"""learning_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views, settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers

from courses import viewset

router = routers.SimpleRouter()
router.register(r'courses', viewset.CourseViewset)
router.register(r'reviews', viewset.ReviewViewSet)


urlpatterns = [
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('suggestions/', views.suggestion_view, name='suggestions'),
    path('admin/', admin.site.urls),
    path('', views.hello, name='home'),

    path('api/v1/courses/', include(('courses.api_urls', 'couses_list'), namespace='courses_list')),
    path('api/v2/', include((router.urls, 'api_v2'), namespace='api_v2')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += staticfiles_urlpatterns()
