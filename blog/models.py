from django.db import models
from django.contrib.auth.models import User

# Create your models here


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class PostAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    viewed = models.BooleanField(blank=True, null=True)


class UserSubscription(models.Model):
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, related_name='authors', on_delete=models.CASCADE, null=True, blank=True)