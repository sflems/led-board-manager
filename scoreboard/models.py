from enum import unique
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
import fastjsonschema, json, os, subprocess
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from constance import config
from django.conf import settings as appSettings
from . import services

# Default User Class
class User(AbstractUser):
    pass

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")

# @receivers create or update Profile model on User model create/update
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.user_profile.save()
    except ObjectDoesNotExist:
        UserProfile.objects.create(user=instance)

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
    
    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

class BoardType(models.Model):
    # Board Choices - NHL/NFL/MLB/custom
    MLB = "MLB"
    NFL = 'NFL'
    NHL = "NHL"
    
    board = models.CharField(
        max_length=16,
        default=NHL,
        primary_key=True,
    )

    path = models.CharField(
        max_length=64,
        default="/home/pi/",
    )

    class Meta:
        verbose_name = _("Board Type")
        verbose_name_plural = _("Boards")
        db_table = 'boardTypes'

    def __str__(self):
        return self.board

    def serialize(self):
        return {
            "board": self.board,
            "path": self.path
        }

class Settings(models.Model):
    name = models.CharField(_("Config Name"), default="Custom Profile Name", max_length=32,)
    config = models.JSONField(default=services.conf_default, blank=True, null=True)
    isActive = models.BooleanField(_("Active"), default=1)
    boardType = models.ForeignKey(BoardType, on_delete=models.CASCADE, default="NHL")
  
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        db_table = 'settings'
        ordering = ["-id"]

        
    def conf_dir(self):
        if os.path.isdir(self.boardType.path + "/config"):
            return os.path.join(self.boardType.path, "config")
        else:
            return self.boardType.path

    def __str__(self):
        return self.name + " Profile"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "config": self.config,
            "isActive": self.isActive,
            "boardType": self.boardType.serialize(),
        }

    def clean(self):
        super().clean()
        
        if self.boardType.board == "NHL":
            try:
                # THIS LINE ONLY CLEANS FORM SAVE DATA ie NOT Settings.object.save()
                # Validate entered config against scoreboard schema from forms.
                fastjsonschema.validate(services.schema(), self.config)
            except fastjsonschema.JsonSchemaException as e:
                raise ValidationError(e)

    def save_to_file(self):
        keepcharacters = (' ', '.', '_')
        filename = "".join(c for c in self.name if c.isalnum() or c in keepcharacters).rstrip().replace(" ", "-") + ".config.json"
        filepath = os.path.join(self.conf_dir(), filename)

        if os.path.isfile(filepath):
            raise ValueError("File with this name already exists. (" + filepath + ")")

        with open(filepath, "w") as outfile:
            json.dump(self.config, outfile, indent=4)
            return filepath

# Checks before model/config save, ie custom validation
@receiver(pre_save, sender=Settings)
def pre_save(sender, instance, *args, **kwargs):

    # Validate config
    instance.full_clean()

    # Raise exception if config directory not found.
    if not os.path.isdir(instance.conf_dir()):
        raise ValueError("Config directory not found.")

    # If config is marked as active, deactivate any other active configs.
    active_profiles = Settings.objects.filter(isActive=True).exclude(name=instance.name)
    if instance.isActive and active_profiles:
        for profile in active_profiles:
            profile.isActive = False
            profile.save()


# Saves config file to nhl-led-scoreboard directory if set as active
@receiver(post_save, sender=Settings)
def post_save(sender, instance, **kwargs):
    if instance.isActive:
        with open(instance.conf_dir() + "/config.json", "w") as outfile:
            json.dump(instance.config, outfile, indent=4)

        # Command attempts to restart scoreboard via supervisorctl
        try:
            if services.proc_status() and not appSettings.TEST_MODE:
                command = "sudo supervisorctl restart " + config.SUPERVISOR_PROGRAM_NAME
                subprocess.check_call(command, shell=True)
            
        except subprocess.CalledProcessError as error:
            return error
