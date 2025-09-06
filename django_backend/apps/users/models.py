from apps.common.models import Team
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=50, default="member")
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,  
        null=True,                   
        blank=True,
        related_name="members"                  
    )

    def __str__(self):
        return self.username
