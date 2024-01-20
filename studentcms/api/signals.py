# your_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    A signal handler that sends a welcome email when a new User is created.
    """
    if created:
        subject = 'Welcome to My Website'
        message = 'Thank you for signing up! We hope you enjoy our website.'
        from_email = 'your@example.com'
        to_email = [instance.email]

        send_mail(subject, message, from_email, to_email)


