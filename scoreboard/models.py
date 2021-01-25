from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.forms import ModelForm, Form
from django_jsonforms.forms import JSONSchemaField
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
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


# TO DO: Implement settings form to change settings and update active profile.
class Settings(models.Model):
    # Opens default config and loads into Settings Profile
    def conf_default():
        with open("./scoreboard/fixtures/config.json.sample", "r") as f:
            return json.load(f)
            
    name = models.CharField(_("Config Name"), default="Default", max_length=32, blank=True)
    config = models.JSONField(default=conf_default)
    isActive = models.BooleanField(_("Active"),default=1)
  
    class Meta:
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")
        
    def __str__(self):
        return self.name + " Profile"
