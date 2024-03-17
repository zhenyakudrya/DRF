from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.serializers.lesson import LessonSerializer
from materials.validators import validator_third_party_resources


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons_list = LessonSerializer(many=True, read_only=True)
    course_content = serializers.CharField(validators=[validator_third_party_resources])
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_content', 'lesson_count', 'lessons_list',  'is_subscribed', 'price']

