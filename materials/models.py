from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, verbose_name='название')
    lesson_content = models.TextField(verbose_name='описание', **NULLABLE)
    lesson_image = models.ImageField(upload_to='materials/', **NULLABLE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, **NULLABLE)
    link_video = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='Пользователь')

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Course(models.Model):
    course_name = models.CharField(max_length=100, verbose_name='наименование')
    course_image = models.ImageField(upload_to='materials/', **NULLABLE)
    course_content = models.TextField(verbose_name='описание')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='Пользователь')
    price = models.PositiveIntegerField(default=10000, verbose_name='Цена курса')

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    status = models.BooleanField(default=False, verbose_name='Статус подписки')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'course')