from django.contrib import admin
from .models import User, Profile, Location

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "location")
    list_display_links = ("user",)
    
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "province", "country",)
    
    

    
# Register your models here.
admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location, LocationAdmin)