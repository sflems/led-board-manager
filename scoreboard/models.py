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


# TO DO: Implement settings form to change settings without having to format as raw JSON, ie. make it easy with choices, selections, etc.
class Settings(models.Model):
    # Opens default config and loads into Settings Profile
    # TO DO: Update default config location to use FileSystemStorage(see Django docs) to load the actual nhl-led-scoreboard install directory config file.
    def conf_default():
        with open("./scoreboard/fixtures/config.json.sample", "r") as f:
            return json.load(f)

    # Model Attributes  
    name = models.CharField(_("Config Name"), default="Default", max_length=32, blank=True)
    configJSON = models.JSONField(default=conf_default())
    isActive = models.BooleanField(_("Active"),default=1)

    conf_default = conf_default()

    # These attributes are generated from the current config schema at build timezone
    # TO DO: Implement a method to create these automatically, or on config schema update
    debug = models.BooleanField(default=conf_default["debug"], null=False, blank=False)
    loglevel = models.CharField(default=conf_default["loglevel"], max_length=16, blank=False)
    live_mode = models.BooleanField(default=conf_default["live_mode"], null=False, blank=False)
    preferences = models.JSONField(default=conf_default["preferences"], null=False)
    states = models.JSONField(default=conf_default["states"], null=False)
    boards = models.JSONField(default=conf_default["boards"], null=False)
    sbio = models.JSONField(default=conf_default["sbio"], null=False)
  
    class Meta:
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")
        db_table = 'settings'
        
    def __str__(self):
        return self.name + " Profile"