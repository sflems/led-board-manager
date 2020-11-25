from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    
class Listing(models.Model):
    title = models.CharField(max_length=128, blank=False, unique=True)
    description = models.CharField(max_length=1000, blank=False)
    image_URL = models.URLField
    start_price = models.PositiveIntegerField
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DurationField(blank=True)
    last_updated = models.DateField(auto_now=True)
    user = User.get(name)
    
class Bids(models.Model):
    pass

class Comments(models.Model):
    listing = models.ForeignKey(Listing, related_name='comments')
    author = models.ForeignKey(User, related_name='author')
    comment = models.CharField(max_length=500, blank=False)
    
class Watchlist(models.Model):
    items = models.ManyToManyField(Listing, blank=True, related_name="watchlist")
    watcher = models.ForeignKey(User, related_name='Watcher')

    def __str__(self):
        return f"{self.items}"