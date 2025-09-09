from django.db.models import Q
from django.utils import timezone
from django.db import models
from apps.users.models import User

class   Tag(models.Model):
    """
    Represents a tag that can be assigned to tasks.

    Attributes:
        name (str): Unique name of the tag.
        description (str): Optional description of the tag.

    Methods:
        __str__(): Returns the name as string representation. 
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name  
    
class TaskQuerySet(models.QuerySet):
    """
    Custom QuerySet for Task model.

    This class provides convinient methods to filter and search tasks
    withot repeating common query logic.

    Methods:
    - active(): returns tasks that are not archived.
    - by_status(status): filters task by status.
    - by_priority(priority): filters tasks by priority.
    - overdue(): returns taks whose due date has passed and are not completed.
    - search(query): performs a search on task titles and descriptions.

    Usage:
        Task.objects.active()
        Task.objects.by_status('todo')
        Task.objects.seach('meeting')

    By using this custom QuerySet, we can chain filters.
    """
    def active(self):
        return self.filter(is_archived=False)

    def by_status(self, status):
        return self.filter(status=status)

    def by_priority(self, priority):
        return self.filter(priority=priority)

    def overdue(self):
        return self.filter(due_date__lt=timezone.now(), status__in=['todo', 'in_progress'])

    # uses Django's Q objects to perform an or operation, the task will be included if
    # either the title or the description matches str
    def search(self, str):
        return self.filter(Q(title__icontains=str) | Q(description__icontains=str))

class TaskManager(models.Manager):
    """
    Custom manager for the Task model.

    This manager provides convinient access to commonly used querysets
    for the Task model by leveraging the custom TaskQuerySet.

    Methods:
    - get_queryset(): Returns a TaskQuerySet instead of the default QuerySet.
    - active(): Returns tasks that are not archived.
    - overdue(): Return tasks that are past their due date and on status 'todo' or 'in_progress'.

    Usage:
        Task.objects.active()
        Task.objects.overdue()
    """
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
    
    def overdue(self):
        return self.get_queryset().overdue()

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

    
class Task(models.Model):
    """
    Represents a task in the system.

    Attributes:
        title (str): Title of the task.
        description (str): Detailed description of the task.
        status (str): Current status of the task.
        priority (str): Priority level of the task.
        due_date (datetime): Deadline for the task completion.
        estimated_hours (Decimal): Estimated time to complete the task.
        actual_hours (Decimal): Actual hours spent.
        created_by (User): User who created the task.
        assigned_to (ManytoMany[User]): Users assigned to the task.
        tags (ManyToMany[Tag]): Tags associated to the task.
        parent_task (Task): Optional parent task for subtasks.
        metadata (dict): Additional JSON metadata.
        created_at (datetime): Task creation timestamp.
        updated_at (datetime): Last update timestamp.
        is_archived (bool): Whether the task is archived.

    Methods:
        __str__(): Returns the title as string representation. 
    """
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

    objects = TaskManager()

    def __str__(self):
        return self.title
    
class TaskAssignment(models.Model):
    """
    Represents assignment of a user to a task.

    Attributes:
        task (Task): Task assigned.
        user (User): User assigned to the task.
        assigned_at (datetime): Timestamp when assigment ocurred.
        assigned_by (User): User who performed the assignment.
        role (str): Role of the assigned user.
    Methods:
        __str__(): Returns a human-readable string representing the username and tha task title assigned. 
    """
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

    # to avoid duplicates
    class Meta:
        unique_together = ("task", "user")

    def __str__(self):
        return f"{self.user.username} -> {self.task.title}"
    
class Comment(models.Model):
    """
    Represents a comment made by a user on a specific task.

    Attributes:
        task (ForeignKey): The Task this comment belongs to.
        author (ForeignKey): The User who authored the comment.
        description (TextField): The content of the comment.
        created_at (DateTimeField): Timestamp when the comment was created.

    Methods:
        __str__(): Returns a human-readable string representing the comment.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"
    
class TaskHistory(models.Model):
    """
    Represents a record of changes made to a task.

    Attributes:
        task (ForeignKey): The Task this history entry belongs to.
        changed_by (ForeignKey): The User who made the change. Can be null.
        field_changed (CharField): The name of the field that was modified.
        old_value (TextField): The previous value of the field.
        new_value (TextField): The new value of the field.
        changed_at (DateTimeField): Timestamp when the change occurred.

    Methods:
        __str__(): Returns a human-readable string representing the history entry.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field_changed = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.task.title} at {self.changed_at}"
    
class TaskTemplate(models.Model):
    """
    Represents a template for creating tasks with default values.

    Attributes:
        name (CharField): Unique name of the task template.
        description (TextField): Description of the template.
        default_priority (CharField): Default priority to assign to tasks created from this template.
        default_estimated_hours (DecimalField): Default estimated hours for tasks created from this template.
        metadata (JSONField): Optional JSON metadata for additional template info.

    Methods:
        __str__(): Returns a human-readable string representing the template.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    default_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    default_estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name