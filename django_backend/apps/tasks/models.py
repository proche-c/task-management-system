from apps.users.models import User
from django.db import models

class   Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name  

STATUS_CHOICES = [
    ("todo", "To Do"),
    ("in_progress", "In Progress"),
    ("done", "Done"),
    ("overdue", "Overdue"),
]

PRIORITY_CHOICES = [
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
    ("critical", "Critical"),
]

# class TaskAssignment(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     assigned_at = models.DateTimeField(auto_now_add=True)
#     assigned_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="assignments_made"
#     )
#     role = models.CharField(max_length=50, default="contributor")

#     class Meta:
#         unique_together = ("task", "user")  # evita duplicados

#     def __str__(self):
#         return f"{self.user.username} -> {self.task.title}"
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateTimeField()
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # Relationships
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_created")
    assigned_to = models.ManyToManyField(
        User,
        through="TaskAssignment",
        through_fields=("task", "user"),
        related_name="tasks_assigned"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
    parent_task = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subtasks"
    )
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assignments_made"
    )
    role = models.CharField(max_length=50, default="contributor")

    class Meta:
        unique_together = ("task", "user")  # evita duplicados

    def __str__(self):
        return f"{self.user.username} -> {self.task.title}"
    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"
    
class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field_changed = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.task.title} at {self.changed_at}"
    
class TaskTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    default_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    default_estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name