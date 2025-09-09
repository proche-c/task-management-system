from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import Task
from apps.users.models import User

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

@shared_task
def generate_daily_summary():
    """Generate daily task summary for all users"""
    yesterday = timezone.now() - timezone.timedelta(days=1)

    for user in User.objects.all():
        created_tasks = Task.objects.filter(created_by=user, created_at__gte=yesterday)
        assigned_tasks = Task.objects.filter(assigned_to=user, updated_at__gte=yesterday)

        tasks_to_summary = []
        if created_tasks.exists():
            tasks_to_summary.append("Tasks created by you:")
            for task in created_tasks:
                tasks_to_summary.append(f"- {task.title} [{task.status}]")
            
        if assigned_tasks.exists():
            tasks_to_summary.append("Tasks assigned to you:")
            for task in assigned_tasks:
                tasks_to_summary.append(f"- {task.title} [{task.status}]")

        summary = "\n".join(tasks_to_summary)
        if user.email:
            send_mail(
                subject="Daily task summary",
                message=summary,
                from_email="noreply@example.com",
                recipient_list=[user.email],

            )
        else:
            print(f"No email for user {user.username}")

generate_daily_summary.delay()