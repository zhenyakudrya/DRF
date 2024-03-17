from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, 'blank': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    verify_code = models.CharField(max_length=12, verbose_name='код активации', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    course = models.ForeignKey('materials.Course', on_delete=models.CASCADE, verbose_name='Курс', related_name='payments',
                               **NULLABLE)
    lesson = models.ForeignKey('materials.Lesson', on_delete=models.CASCADE, verbose_name='Урок', related_name='payments',
                               **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('transfer', 'Transfer')],
                                      verbose_name='Способ оплаты'),
    url_payment = models.CharField(max_length=500, default='', verbose_name='Ссылка на оплату'),
    status = models.CharField(max_length=1, default='P', choices=[('P', 'Process'), ('S', 'Success'), ('C', 'Canceled')],
                              verbose_name='Статус оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Пользователь {self.user} оплатил курс {self.course} на сумму {self.amount}'