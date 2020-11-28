from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

class User(AbstractUser):
    pass
    
class Listing(models.Model):
    title = models.CharField(max_length=128, blank=False, unique=True)
    description = models.TextField(max_length=1000, blank=False)
    image_URL = models.URLField(blank=True)
    start_bid = models.DecimalField(max_digits=12, decimal_places=2, default="00.00")
    current_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='current_bid', blank=True, null=True)
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='current_bid', blank=True, null=True)
    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='sellers')
    
    def __str__(self):
        return f"{self.title}"
    
class Bid(models.Model):
    bid = models.DecimalField(max_digits=12, decimal_places=2, default="00.00")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidders')
    created = models.DateTimeField(editable=False, default=timezone.now)
    
    def __str__(self):
        return f"{self.bid} by {self.user}"
        
class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ("bid",)
        labels = {
            "bid": _("New Bid"),
        }

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    comment = models.CharField(max_length=500, blank=False)
    created = models.DateTimeField(editable=False, default=timezone.now)
    
    def __str__(self):
        return f"{self.comment} - By: {self.user} - ({self.modified})"
    
class Watchlist(models.Model):
    items = models.ManyToManyField(Listing, blank=True, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchers')

    def __str__(self):
        return f"{self.user}'s Watchlist: {self.items}"