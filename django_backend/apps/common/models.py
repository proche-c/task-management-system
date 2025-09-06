from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50, default="other", unique=True)

    def __str__(self):
        return self.name

    

    
