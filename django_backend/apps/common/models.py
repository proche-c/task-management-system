from django.db import models

class Team(models.Model):
    """
    Represent a team in the system.

    Attributes:
        name (str): The unique name of the team. Default is 'other'.

    Methods:
        __str__(): Returns the team's name as its string representation.
    """
    name = models.CharField(max_length=50, default="other", unique=True)

    def __str__(self):
        return self.name

    

    
