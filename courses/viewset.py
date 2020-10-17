from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action

from . import models
from .serializers import CourseSerializer, ReviewSerializer


# reduced version of the one bellow
class ListCreateCourseGenerics(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


class ListCreateReview(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.queryset.filter(course__id=self.kwargs.get('course_pk'))

    # prevent a user to post a review to another course
    def perform_create(self, serializer):
        course = get_object_or_404(models.Course, pk=self.kwargs.get('course_pk'))
        serializer.save(course=course)


class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            course_id=self.kwargs.get('course_pk'),
            pk=self.kwargs.get('pk')
        )


# not in use currently
class ListCreateCourse(APIView):
    def get(self, request, format=None):
        courses = models.Course.objects.all()
        serializers = CourseSerializer(courses, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Using Viewsets
class CourseViewset(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        self.pagination_class.page_size = 1
        reviews = models.Review.objects.filter(course_id=pk)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ReviewSerializer(reviews, many=True)
        # course = self.get_object()
        # serializer = ReviewSerializer(course.reviews.all(), many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer
