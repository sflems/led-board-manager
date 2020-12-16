from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    about = models.TextField(max_length=300, blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Profiles"
        
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Location(models.Model):
    city = models.TextField(max_length=300, blank=True)
    province = models.TextField(max_length=2, blank=True)
    country = models.TextField(max_length=30, blank=False)
    
    class Meta:
        verbose_name_plural = "Locations"
        
    def __str__(self):
        return f"{self.city.title()}, {self.province.upper()}, {self.country.title()}"
        
class Post(models.Model):
    title = models.CharField(max_length=128, blank=False, unique=True)
    content = models.TextField(max_length=1000, blank=False)
    image_URL = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)
    author = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='post_authors')
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
        
    def serialize(self):
        '''TODO: Define serialize() for Post. See Project 3's mail.models.Email for reference'''
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "image_URL": self.image_URL,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "modified": self.modified,
            "is_active": self.is_active,
            "author": self.author.username
        }
        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "image_URL",)
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_authors')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_list')
    comment = models.TextField(max_length=500, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.comment} - By: {self.user} - ({self.created})"

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
        labels = {
            "comment": _("New comment"),
        }

class FollowingList(models.Model):
    followed_users = models.ManyToManyField(User, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"{self.user}'s Following List"
