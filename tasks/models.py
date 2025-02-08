from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Projects Table
class Project(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining auto-incrementing primary key
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Modified Task Table with project_id relationship
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='tasks')
    
    def __str__(self):
        return self.title
