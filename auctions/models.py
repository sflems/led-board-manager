from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

class User(AbstractUser):
    pass
    
class Category(models.Model):
    name = models.CharField(max_length=128, blank=False, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"
    
class Listing(models.Model):
    title = models.CharField(max_length=128, blank=False, unique=True)
    description = models.TextField(max_length=1000, blank=False)
    image_URL = models.URLField(blank=True)
    category = models.ManyToManyField('Category', related_name='categories', blank=True,)
    start_bid = models.DecimalField(max_digits=12, decimal_places=2, default="00.00")
    current_bid = models.OneToOneField('Bid', on_delete=models.SET_NULL, related_name='current_bid', blank=True, null=True,)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='sellers')
    
    def __str__(self):
        return f"{self.id}: {self.title}"
        
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ("title", "description", "image_URL", "category", "start_bid",)
        labels = {
            "start_bid": _("Starting Bid"),
        }
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bid_list')
    bid = models.DecimalField(max_digits=12, decimal_places=2, default="00.00")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidders')
    created = models.DateTimeField(auto_now_add=True)
    winning_bid = models.BooleanField(default=0)
    
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
    listing_title = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comment_list')
    comment = models.TextField(max_length=500, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.comment} - By: {self.user} - ({self.created})"

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
        labels = {
            "comment": _("New comment"),
        }    
class Watchlist(models.Model):
    items = models.ManyToManyField(Listing, related_name="item_list", blank=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watcher')

    def __str__(self):
        return f"{self.user}'s Watchlist"