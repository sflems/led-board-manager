from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.forms import ModelForm
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

# Default User Class
class User(AbstractUser):
    pass

# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

# @receivers create or update Profile model on User model create/update
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
        
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)