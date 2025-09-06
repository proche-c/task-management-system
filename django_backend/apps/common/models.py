from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50, default="other", unique=True)

    def __str__(self):
        return self.name

    
    
# class Comment(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Comment by {self.author.username} on {self.task.title}"
    
# class TaskHistory(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history")
#     changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     field_changed = models.CharField(max_length=100)
#     old_value = models.TextField(null=True, blank=True)
#     new_value = models.TextField(null=True, blank=True)
#     changed_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"History for {self.task.title} at {self.changed_at}"
    
# class TaskTemplate(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField()
#     default_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
#     default_estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
#     metadata = models.JSONField(default=dict, blank=True)

#     def __str__(self):
#         return self.name