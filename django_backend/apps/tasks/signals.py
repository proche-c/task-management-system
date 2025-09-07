from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task, TaskHistory

@receiver(pre_save, sender=Task)
def create_task_history(sender, instance, **kwargs):
    """
    Registration of task updates before saving.
    """
    if not instance.pk:
        return

    previous = Task.objects.get(pk=instance.pk)
    changes = []

    fields_to_track = [
        "title", "description", "status", "priority", "due_date", "estimated_hours",
        "actual_hours", "is_archived", "parent_task_id", "assigned_to", "tags", "is_archived"
    ]

    for field in fields_to_track:
        old = getattr(previous, field)
        new = getattr(instance, field)
        if old != new:
            changes.append((field, old, new))

    for field, old, new in changes:
        TaskHistory.objects.create(
            task=instance,
            changed_by=getattr(instance, 'updated_by', None),
            field_changed=field,
            old_value=old,
            new_value=new
        )