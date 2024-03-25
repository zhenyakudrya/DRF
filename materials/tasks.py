from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from celery import shared_task
from materials.models import Subscription


@shared_task
def send_email_update_course(course_id):
    subscriptions = Subscription.objects.all().filter(course_id=course_id)
    users = []
    for subscription in subscriptions:
        users.append(subscription.user)
    for user in users:
        message = f"Привет {user.first_name} {user.last_name}. {course_id} был обновлен."
        send_mail(
            subject="Course's update",
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )