from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import *
import json, os
from . import services

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

class Settings(models.Model):
    name = models.CharField(_("Config Name"), default="Custom Profile Name", max_length=32, blank=True, unique=True)
    config = models.JSONField(default=services.conf_default())
    isActive = models.BooleanField(_("Active"),default=1)
  
    class Meta:
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")
        db_table = 'settings'
        
    def __str__(self):
        return self.name + " Profile"

@receiver(pre_save, sender=Settings)
def pre_save(sender, instance, **kwargs):
    active_profiles = Settings.objects.filter(isActive=True).exclude(name=instance.name)
    if instance.isActive and active_profiles:
            for profile in active_profiles:
                profile.isActive = False
                profile.save()

# TO DO: Implement method of changing config path. Is a reboot necessary? Also add a static default config file for good measure.
@receiver(post_save, sender=Settings)
def post_save(sender, instance, **kwargs):
    if instance.isActive:
        with open(services.install_path() + "/config.json", "w") as outfile:
            # indent=4 makes content human readable
            json.dump(instance.config, outfile, indent=4)
            
    
@receiver(pre_delete, sender=Settings)
def delete_is_default(sender, instance, **kwargs):
    if instance.name.lower() == "default":
       raise FieldError('Default profile is read-only. Profile not removed.')
