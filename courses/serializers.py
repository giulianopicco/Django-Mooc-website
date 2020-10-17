from rest_framework import serializers

from . import models


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }
        fields = (
            'id',
            'course',
            'name',
            'email',
            'comment',
            'rating',
            'created_at',
        )
        model = models.Review


class CourseSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    # reviews = serializers.HyperlinkedRelatedField(view_name='api_v2:review-detail', many=True, read_only=True)
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        fields = (
            'id',
            'teacher',
            'created_at',
            'title',
            'description',
            'published',
            'status',
            'subject',
            'reviews',
        )
        model = models.Course
