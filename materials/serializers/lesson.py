from rest_framework import serializers

from materials.models import Lesson, Course
from materials.validators import validator_third_party_resources


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    lesson_content = serializers.CharField(validators=[validator_third_party_resources])
    # link_video = serializers.CharField(validators=[validator_third_party_resources])
    class Meta:
        model = Lesson
        fields = '__all__'
