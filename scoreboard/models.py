import fastjsonschema, json, os, subprocess
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.conf import settings as appSettings

import logging

logger = logging.getLogger('django')


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
        max_length=128,
        default=os.path.expanduser("~"),
    )

    startupActive = models.BooleanField(default=False)

    supervisorName = models.CharField(
        max_length=32,
        unique=True,
    )

    class PythonVersion(models.TextChoices):
        TWO = 2
        THREE = 3
    pythonVersion = models.CharField(default=3, max_length=1, blank=True, choices=PythonVersion.choices)

    class Meta:
        verbose_name = _("Board")
        verbose_name_plural = _("Boards")
        db_table = 'boardTypes'

    def conf_dir(self):
        if os.path.isdir(self.path + "/config"):
            return os.path.join(self.path, "config")
        else:
            return self.path

    def main(self):
        if os.path.isdir(os.path.join(self.path, "src")):
            return os.path.join(".", "src", "main.py")
        else:
            return os.path.join(".", "main.py")

    def schema(self):
        schemaPath = os.path.join(self.conf_dir(), 'config.schema.json')
        if os.path.isfile(schemaPath):
            with open(schemaPath, "r") as f:
                schema = json.load(f)
                return schema
        return {}

    def configJSON(self):
        confPath = os.path.join(self.conf_dir(), 'config.json')
        if os.path.isfile(confPath):
            with open(confPath, "r") as f:
                        config = json.load(f)
                        return config
        return {}

    def proc_status(self):
        command = "sudo supervisorctl status boards:" + self.supervisorName
        process = subprocess.run(command, shell=True, capture_output=True)

        return b'RUNNING' in process.stdout

    def __str__(self):
        return self.board

    def serialize(self):
        return {
            "board": self.board,
            "path": self.path,
            "startupActive": self.startupActive,
            "supervisorName": self.supervisorName,
            "activeConfig": self.configJSON(),
            "schema": self.schema(),
        }

@receiver(pre_save, sender=BoardType)
def pre_save_board_type(sender, instance, *args, **kwargs):
    if instance.path.startswith("~"):
        stripped = instance.path.strip("~")
        instance.path = os.path.expanduser("~") + stripped

class Settings(models.Model):
    name = models.CharField(_("Config Name"), default="Custom Profile Name", max_length=32)
    config = models.JSONField(default=dict, blank=True, null=True)
    isActive = models.BooleanField(_("Active"), default=1)
    boardType = models.ForeignKey(BoardType, related_name="profiles", on_delete=models.CASCADE, to_field="board", default="NHL")

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        db_table = 'settings'
        ordering = ["-id"]

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
        if self.isActive:
            fastjsonschema.validate(self.boardType.schema(), self.config)

    def save_to_file(self):
        keepcharacters = (' ', '.', '_')
        filename = "".join(c for c in self.name if c.isalnum() or c in keepcharacters).rstrip().replace(" ", "-") + ".config.json"
        filepath = os.path.join(self.boardType.conf_dir(), filename)

        if os.path.isfile(filepath):
            raise ValueError("File with this name already exists. (' {} ')".format(filename))

        with open(filepath, "w") as outfile:
            json.dump(self.config, outfile, indent=4)
            return filepath

# Checks before model/config save, ie custom validation
@receiver(pre_save, sender=Settings)
def pre_save(sender, instance, *args, **kwargs):

    # Validate config
    try:
        instance.full_clean()
    except (fastjsonschema.JsonSchemaException, Exception) as e:
        logger.exception(e)
        raise ValidationError(e)

    # Raise exception if config directory not found.
    if not os.path.isdir(instance.boardType.conf_dir()):
        raise ValueError("Config directory not found. Dir: " + instance.boardType.conf_dir())

    # If config is marked as active, deactivate any other active configs.
    active_profiles = Settings.objects.filter(isActive=True).exclude(pk=instance.id)
    if instance.isActive:
        if active_profiles:
            active_profiles.update(isActive=False)


# Saves config file to nhl-led-scoreboard directory if set as active
@receiver(post_save, sender=Settings)
def post_save(sender, instance, **kwargs):
    if instance.isActive:
        active_boards = BoardType.objects.filter(board=instance.boardType)
        inactive_boards = BoardType.objects.all().exclude(board=instance.boardType)

        active_boards.update(startupActive=True)
        inactive_boards.update(startupActive=False)

        with open(instance.boardType.conf_dir() + "/config.json", "w") as outfile:
            json.dump(instance.config, outfile, indent=4)

        # Command attempts to restart scoreboard via supervisorctl
        try:
            if not appSettings.TEST_MODE:
                command = "sudo supervisorctl stop boards:*"
                subprocess.check_call(command, shell=True)

                command2 = "sudo supervisorctl start boards:" + instance.boardType.supervisorName
                subprocess.check_call(command2, shell=True)

        except subprocess.CalledProcessError as error:
            raise Exception(error)
