from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    
class Listing(models.Model):
    title = models.CharField(max_length=128, blank=False, unique=True)
    description = models.TextField(max_length=1000, blank=False)
    image_URL = models.URLField(blank=True)
    start_bid = models.DecimalField(max_digits=12, decimal_places=2, default="00.00")    
    current_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='listings', null=True) 
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=False)
    last_updated = models.DateField(auto_now=True)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='sellers')
    
    def __str__(self):
        return f"{self.title} - ${self.start_bid}"
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listings', null=True)
    bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='bidder')
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.listing.id}: {self.listing} - {self.user} - Bid: {self.bid}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    comment = models.CharField(max_length=500, blank=False)
    
    def __str__(self):
        return f"Listing: {self.listing} - {self.comment} - By: {self.user}"
    
class Watchlist(models.Model):
    items = models.ManyToManyField(Listing, blank=True, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchers')

    def __str__(self):
        return f"{self.user}"