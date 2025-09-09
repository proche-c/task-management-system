from rest_framework import serializers
from apps.tasks.models import Tag, TaskAssignment, Comment, TaskHistory, TaskTemplate, Task
from apps.users.api.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.

    Converts Tag instances to JSON.

    Fields:
        id (int): Primary key of the tag.
        name (str): Name of the tag.
        description (str): Optional description of the tag.
    """
    class Meta:
        model = Tag
        fields = ["id", "name", "description"]

class TaskAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the TaskAssignment model.

    Includes information about which user is assigned to a task, who
    assigned them, and their role.

    Fields:
        id (int): Primary key of the assignment.
        task (int): Task id
        user (User): Assigned user (read-only)
        assigned_by (User): User who made the assignment (read-only).
        role (str): Role of the assigned user.
    """
    user = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)

    class Meta:
        model = TaskAssignment
        fields = ["id", "task", "user", "assigned_at", "assigned_by", "role"]

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    Represents comments made by users on tasks.

    Fields:
        id (int): Primary key of the comment
        task (int): ID of the related task (read-only)
        author (User): User who made the comment (nested UserSerializer, read-only)
        description (str): Content of the comment
        created_at (datetime): Timestamp when the comment was created
    """
    author = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "task", "author", "description", "created_at"]

class TaskHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the TaskHistory model.

    Tracks changes made to tasks, including who made the change and what was changed.

    Fields:
        id (int): Primary key of the history record
        task (int): Related task ID
        changed_by (User): User who made the change (nested UserSerializer, read-only)
        field_changed (str): Name of the field that changed
        old_value(str): Previous value of the field
        new_value (str): New value of the field
        changed_at (datetime): Timestamp of the change
    """
    changed_by = UserSerializer(read_only=True)

    class Meta:
        model = TaskHistory
        fields = ["id", "task", "changed_by", "field_changed", "old_value", "new_value", "changed_at"]

class TaskTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for the TaskTemplate model.

    Represents predefined task templates to simplify task creation.

    Fields:
        id (int): Primary key of the template
        name (str): Name of the template
        description (str): Description of the template
        default_priority (str): Default priority assigned when using this template
        default_estimated_hours (Decimal): Default estimated hours for tasks created from this template
        metadata (JSON): Optional JSON metadata
    """
    class Meta:
        model = TaskTemplate
        fields = ["id", "name", "description", "default_priority", "default_estimated_hours", "metadata"]

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Fully represents a task, including related users, tags, comments, and history.

    Fields:
        id (int): Primary key of the task
        title (str): Task title
        description (str): Task description
        status (str): Current status of the task
        priority (str): Task priority
        due_date (datetime): Task due date
        estimated_hours (Decimal): Estimated hours to complete
        actual_hours (Decimal): Actual hours spent
        created_by (User): User who created the task (nested UserSerializer, read-only)
        assigned_to (User): Users assigned to the task (nested UserSerializer, read-only)
        tags (Tags[]): Tags related to the task (nested TagSerializer, read-only)
        parent_task (int): Optional parent task
        metadata (JSON): Optional JSON metadata
        created_at (datetime): Timestamp when the task was created
        updated_at (datetime): Timestamp when the task was last updated
        is_archived (bool): Boolean indicating if the task is archived
        comments (Comment[]): Comments on the task (nested CommentSerializer, read-only)
        history: Task change history (nested TaskHistorySerializer, read-only)
    """
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    history = TaskHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "estimated_hours",
            "actual_hours",
            "created_by",
            "assigned_to",
            "tags",
            "parent_task",
            "metadata",
            "created_at",
            "updated_at",
            "is_archived",
            "comments",
            "history",
        ]
