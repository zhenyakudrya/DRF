from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, verbose_name='название')
    lesson_content = models.TextField(verbose_name='описание')
    lesson_image = models.ImageField(upload_to='materials/', **NULLABLE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    link_video = models.URLField(verbose_name='ссылка на видео')

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Course(models.Model):
    course_name = models.CharField(max_length=100, verbose_name='наименование')
    course_image = models.ImageField(upload_to='materials/', **NULLABLE)
    course_content = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'