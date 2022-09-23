from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="following")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs): 
        instance.profile.save()

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
