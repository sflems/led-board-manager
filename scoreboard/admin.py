from django.contrib import admin, messages
from .models import Settings, Team, User
from .forms import SettingsDetailForm, SettingsJSONForm

# Tests if a profile is selected as active. Otherwise sets to default profile.
def delete_selected(SettingsAdmin, request, queryset):
    try:
        for obj in queryset:
            if obj.name.lower() != "default":
                obj.delete()
    except:
        pass  

# TO DO: Change default admin form to JSONForm
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'isActive')
    list_display_links = ('id', 'name',)
    actions = [delete_selected]

    def get_readonly_fields(self, request, obj):
        try:
            if obj.name.lower() != "default": 
                return self.readonly_fields
            return self.readonly_fields + ('name', 'config')
        except:
            return self.readonly_fields

    # Checks to see if active profile status changed, and then makes it the only active profile if so.
    def save_model(self, request, obj, form, change):
        if obj.isActive:
            if Settings.objects.filter(isActive=True):
                active_profiles = Settings.objects.filter(isActive=True).exclude(name=obj.name)
                for profile in active_profiles:
                    profile.isActive = False
                    profile.save()


            '''
            Insert filesystem saving logic (and scoreboard restart logic?) here.
            '''

            obj.save()
            super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change) 

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'teamName', 'abbreviation',)
    ordering = ('teamName',)
    readonly_fields = ('name', 'abbreviation', 'teamName', 'locationName', 'jsonLink', 'officialSiteUrl')

# Register your models here.
admin.site.register(User)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Team, TeamAdmin)
