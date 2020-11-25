from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    
class Listing(models.Model):
    title = models.CharField(max_length=128, blank=False, unique=True)
    description = models.TextField(max_length=1000, blank=False)
    image_URL = models.URLField(blank=True)
    start_price = models.DecimalField(max_digits=12, decimal_places=2, default="00.00")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=False)
    last_updated = models.DateField(auto_now=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    
class Bid(models.Model):
    pass

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    comment = models.CharField(max_length=500, blank=False)
    
class Watchlist(models.Model):
    items = models.ManyToManyField(Listing, blank=True, related_name="watchlist")
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Watcher')

    def __str__(self):
        return f"{self.items}"