from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import *
import json

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

# Fixtures - import from JSON with manage.py loaddata
class Team(models.Model):      
    name = models.CharField(max_length=32, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True, null=True)
    teamName = models.CharField(max_length=32, null=True)
    locationName = models.CharField(max_length=32, null=True)
    jsonLink = models.URLField(null=True)
    officialSiteUrl = models.URLField(null=True)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Team_detail", kwargs={"pk": self.pk})


# TO DO: Implement saving of updated config data, and save it in a location used by the led-scoreboard. Is a reboot necessary?
class Settings(models.Model):

    # Opens default config and loads into Settings Profile
    # TO DO: Update default config location to use FileSystemStorage(see Django docs) to load the actual nhl-led-scoreboard install directory config file.
    def conf_default():
        with open("/home/flem/nhl-led-scoreboard/config/config.json.sample", "r") as f:
            conf = json.load(f)
            return conf

    # Model Attributes 
    name = models.CharField(_("Config Name"), default="Custom Profile Name", max_length=32, blank=True, unique=True)
    config = models.JSONField(default=conf_default)
    isActive = models.BooleanField(_("Active"),default=1)
  
    class Meta:
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")
        db_table = 'settings'
        
    def __str__(self):
        return self.name + " Profile"

@receiver(pre_delete, sender=Settings)
def delete_is_default(sender, instance, **kwargs):
    if instance.name.lower() == "default":
       raise ValueError('Default profile is read-only. Profile not removed.')


    # TO DO: Define the save method to allow only one active profile here. Currently validation happens in both views.py and admin.py

