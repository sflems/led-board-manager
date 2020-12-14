from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=300, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

class Location(models.Model):
    city = models.TextField(max_length=300, blank=True)
    province = models.TextField(max_length=2, blank=True)
    country = models.TextField(max_length=30, blank=True)
    
    def __str__(self):
        return f"{self.city.title()}, {self.province.upper()}, {self.country.title()}"
