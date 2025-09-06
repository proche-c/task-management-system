from rest_framework import serializers
from apps.tasks.models import Tag, TaskAssignment, Comment, TaskHistory, TaskTemplate, Task
from apps.users.api.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "description"]

class TaskAssignmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)

    class Meta:
        model = TaskAssignment
        fields = ["id", "task", "user", "assigned_at", "assigned_by", "role"]

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "task", "author", "description", "created_at"]

class TaskHistorySerializer(serializers.ModelSerializer):
    changed_by = UserSerializer(read_only=True)

    class Meta:
        model = TaskHistory
        fields = ["id", "task", "changed_by", "field_changed", "old_value", "new_value", "changed_at"]

class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = ["id", "name", "description", "default_priority", "default_estimated_hours", "metadata"]

class TaskSerializer(serializers.ModelSerializer):
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
