from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.serializers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons_list = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lesson_count', 'lessons_list']

