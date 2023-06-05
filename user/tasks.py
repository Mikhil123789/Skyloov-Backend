from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
from celery import shared_task
from . import models
import datetime
from django.utils import timezone

# app = Celery('tasks', broker='pyamqp://guest@localhost//')

@shared_task(name="add_two_values")
def add(x, y):
    return x + y


@shared_task(name="send_email")
def send_email():
    """Send email to user after 1 day of registration"""
    try:
        one_day_ago = timezone.now() - datetime.timedelta(days=1)
        user_obj = models.User.objects.filter(is_notified=False, created_at__lte=one_day_ago)
        if user_obj:
            for user_ in user_obj:
                send_mail(
                        "Welcome to Skyloov Portal",
                        f'Hello {user_.first_name},\n\nWelcome to Skyloov Portal! We are excited to have you on board.\nIf you have any questions or need assistance, feel free to reach out to our support team.\n\nBest regards,\nThe Skyloov Team',
                        "developer.mikhi@gmail.com",
                        [user_.email],
                        fail_silently=False,
                    )
                user_.is_notified = True
                user_.save()
        else:
            pass
    except Exception as e:
        print(str(e))

