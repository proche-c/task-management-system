from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import Task

@shared_task
def send_task_notification(task_id, notification_type):
    """Send email notifications for task events"""
    try:
        task = Task.objects.get(id=task_id)
        users_emails = list(task.assigned_to.values_list("email", flat=True))
        if task.created_by and task.created_by.email:
            users_emails.append(task.created_by.email)
        users_emails = list(set(users_emails))

        if not users_emails:
            print("No destinatary for notification")

        send_mail(
            "Task notification",
            f'Notification: task {task.title} {notification_type}',
            "noreply@example.com",
            users_emails,
        )
    except Task.DoesNotExist:
        print("Task doesn't exist")