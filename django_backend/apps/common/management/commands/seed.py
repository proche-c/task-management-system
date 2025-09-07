from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.common.models import Team
from apps.tasks.models import Task, Tag, Comment, TaskHistory, TaskTemplate, TaskAssignment
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = "Seed database with initial data (teams, users, tags, tasks, etc.)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        # --- Teams ---
        team_dev, _ = Team.objects.get_or_create(name="Development")
        team_ops, _ = Team.objects.get_or_create(name="Operations")

        # --- Users ---
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "role": "admin",
                "team": team_dev,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password("admin123")
            admin.save()

        user1, _ = User.objects.get_or_create(
            username="alice",
            defaults={"email": "alice@example.com", "role": "member", "team": team_dev},
        )
        user1.set_password("alice123")
        user1.save()

        user2, _ = User.objects.get_or_create(
            username="bob",
            defaults={"email": "bob@example.com", "role": "member", "team": team_ops},
        )
        user2.set_password("bob123")
        user2.save()

        # --- Tags ---
        bug_tag, _ = Tag.objects.get_or_create(name="bug", defaults={"description": "Bug fixing"})
        feature_tag, _ = Tag.objects.get_or_create(name="feature", defaults={"description": "New feature"})
        urgent_tag, _ = Tag.objects.get_or_create(name="urgent", defaults={"description": "Needs immediate attention"})

        # --- Tasks ---
        task1, _ = Task.objects.get_or_create(
            title="Fix login issue",
            defaults={
                "description": "Resolve 500 error when logging in",
                "status": "in_progress",
                "priority": "high",
                "due_date": timezone.now() + timedelta(days=3),
                "estimated_hours": 5,
                "created_by": admin,
            },
        )
        task1.tags.add(bug_tag, urgent_tag)
        TaskAssignment.objects.get_or_create(task=task1, user=user1, assigned_by=admin)

        task2, _ = Task.objects.get_or_create(
            title="Implement dashboard",
            defaults={
                "description": "Create task dashboard page",
                "status": "todo",
                "priority": "medium",
                "due_date": timezone.now() + timedelta(days=7),
                "estimated_hours": 12,
                "created_by": user1,
            },
        )
        task2.tags.add(feature_tag)
        TaskAssignment.objects.get_or_create(task=task2, user=user2, assigned_by=user1)

        # --- Comments ---
        Comment.objects.get_or_create(task=task1, author=user1, description="I’m checking the logs")
        Comment.objects.get_or_create(task=task2, author=user2, description="Started UI design")

        # --- Task History ---
        TaskHistory.objects.get_or_create(
            task=task1,
            changed_by=admin,
            field_changed="status",
            old_value="todo",
            new_value="in_progress",
        )

        # --- Task Templates ---
        TaskTemplate.objects.get_or_create(
            name="Bug fix template",
            defaults={
                "description": "Default structure for bug fixes",
                "default_priority": "high",
                "default_estimated_hours": 4,
                "metadata": {"type": "bug"},
            },
        )
        TaskTemplate.objects.get_or_create(
            name="Feature template",
            defaults={
                "description": "Template for new feature development",
                "default_priority": "medium",
                "default_estimated_hours": 10,
                "metadata": {"type": "feature"},
            },
        )

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))