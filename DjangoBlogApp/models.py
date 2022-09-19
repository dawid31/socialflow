from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=48, blank=True, null=True)
    content = models.TextField(max_length=512)
    likes = models.ManyToManyField(User, blank=True, related_name="blog_posts")
    img = models.ImageField(null=True, blank=True, upload_to = "images/")
    host = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)
    
    class Meta():
        ordering = ['-published']

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    biogram = models.TextField(max_length=512)
    avatar = models.ImageField(null=True, blank=True, default='default.png')
    
    
    def __str__(self):
        return f"{self.user.username} profile"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(max_length=128, blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['published']

    def __str__(self):
        return f"{self.author} comment: {self.content}"
