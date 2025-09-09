from apps.common.models import Team
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending AbstractUser.

    Attributes:
        role (str): The role of the user in the system, e.g., 'member', 'admin'.
        team (Team, optional) : Reference to the team the user belong to.
            Can be null or blank. Deleting a team sets this field to null.
    Methods:
        __str__(): Returns the username as string representation. 
    """
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
