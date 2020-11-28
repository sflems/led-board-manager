from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watchlist

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "start_bid", "current_bid", "user")
    list_display_links = ("title",)
    
# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)