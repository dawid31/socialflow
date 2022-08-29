from django.db import models
    
# Create your models here.
from django.contrib.auth.models import User

class Post(models.Model):
    name = models.CharField(max_length=32)
    content = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)
    
    class Meta():
        ordering = ['-published']

    def __str__(self):
        return f"{self.name}"
