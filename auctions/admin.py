from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watchlist, Category

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "start_bid", "current_bid", "user")
    list_display_links = ("title",)
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "bid", "user")
    list_display_links = ("bid",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "comment", "user")
    list_display_links = ("comment",)    

    
# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist)
admin.site.register(Category)