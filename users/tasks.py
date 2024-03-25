from celery import shared_task
from users.models import User
from datetime import timedelta, timezone


@shared_task
def check_all_users_last_login():
    date_x = timezone.now() - timedelta(days=30)
    users_to_deactivate = User.objects.filter(last_login__lt=date_x)
    for user in users_to_deactivate:
        user.is_active = False
        user.save()
        print(f"{user} был заблокирован")