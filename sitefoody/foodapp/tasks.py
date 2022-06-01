from django.core.mail import send_mail
from sitefoody.celery import app
from .models import *
from decouple import config


@app.task
def first_message_distribution(user_email):
    send_mail('Site foody',
              'Вы подписались на рассылку',
              config('EMAIL_HOST_USER'),
              [user_email],
              fail_silently=False)


@app.task
def mailing_list():
    send_mail('Site foody',
              'Приходите в наш ресторан',
              config('EMAIL_HOST_USER'),
              [email_model.email for email_model in EmailForDistribution.objects.all()],
              fail_silently=False)
