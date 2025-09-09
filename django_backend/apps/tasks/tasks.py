from datetime import timedelta
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

@shared_task
def check_overdue_tasks():
    """Mark tasks as overdue and notify assignees"""
    now = timezone.now()
    overdue_tasks = Task.objects.filter(due_date__lt=now).exclude(status='completed')

    for task in overdue_tasks:
        if task.status != 'overdue':
            task.status = 'overdue'
            task.save(update_fields=['status'])

        for user in task.assigned_to.all():
            if user.email:
                send_mail(
                    subject=f"Task Overdue: {task.title}",
                    message=f"The task '{task.title}' was due on {task.due_date.strftime('%Y-%m-%d %H:%M')} and is now overdue.",
                    from_email="noreply@example.com",
                    recipient_list=[user.email],
                )

@shared_task
def cleanup_archived_tasks():
    """
    Delete archived tasks older than 30 days.
    """
    cutoff_date = timezone.now() - timedelta(days=30)
    old_archived_tasks = Task.objects.filter(is_archived=True, updated_at__lt=cutoff_date)
    old_archived_tasks.delete()

    return f"Archived tasks older than 30 days were deleted."