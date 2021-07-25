from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Post)
def my_handler(sender, **kwargs):
    post = kwargs['instance']

    if post.author:
        author = post.author
        subscribers = UserSubscription.objects.filter(author=author)

        emails = []
        for subscriber in subscribers:
            emails.append(subscriber.user.email)

        subject = 'New post'
        html_message = render_to_string('email.html', {'post': post})
        to = emails

        msg = EmailMultiAlternatives(
            subject,
            html_message,
            to=to,
        )

        msg.attach_alternative(html_message, "text/html")
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'

        msg.send(fail_silently=False)
