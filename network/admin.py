from django.contrib import admin
from .models import User, Profile, Location, Post, Comment, FollowingList

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "location")
    list_display_links = ("user",)
    
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "province", "country",)
    
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author",)
    list_display_links = ("id",)
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "comment", "user")
    list_display_links = ("comment",) 
    
    
# Register your models here.
admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FollowingList)