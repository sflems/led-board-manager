import fastjsonschema
from prettyjson import PrettyJSONWidget
from django.contrib import admin, messages
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist
from django.db import models
from django.http import HttpResponseRedirect
from .models import Settings, Team, User


# Tests if a profile is selected as active. Otherwise sets to default profile.
def delete_selected(SettingsAdmin, request, queryset):
    try:
        for obj in queryset:
            if obj.name.lower() != "default" and obj.isActive is not True:
                obj.delete()
    except EmptyResultSet:
        pass

class SettingsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': PrettyJSONWidget(attrs={'initial': 'parsed'})}
    }
    list_display = ('id', 'name', 'isActive')
    list_display_links = ('id', 'name',)
    actions = [delete_selected]

    # Defines default settings model profile as read-only
    def get_readonly_fields(self, request, obj):
        try:
            if obj.name.lower() != "default":
                return self.readonly_fields
            return self.readonly_fields + ('name', 'config')
        except ObjectDoesNotExist:
            return self.readonly_fields

    # Defines delete permissions. Returns a delete button for Settings models as long as there are models present AND they aren't the default profile.
    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and (not obj or obj.name.lower() != 'default')
            
    # Checks to see if active profile status changed, and then makes it the only active profile if so.
    def save_model(self, request, obj, form, change):
        try:
            if obj.isActive:
                
                # Checks if there are other active profiles and deactivates them.
                if Settings.objects.filter(isActive=True):
                    active_profiles = Settings.objects.filter(isActive=True).exclude(name=obj.name)
                    for profile in active_profiles:
                        profile.isActive = False
                        profile.save()

                obj.save()
                super().save_model(request, obj, form, change)
            else:
                super().save_model(request, obj, form, change)
        except fastjsonschema.JsonSchemaValueException as e:
            self.message_user(request, e, level=messages.ERROR)
            return HttpResponseRedirect(request)


'''
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'teamName', 'abbreviation',)
    ordering = ('teamName',)
    readonly_fields = ('name', 'abbreviation', 'teamName', 'locationName', 'jsonLink', 'officialSiteUrl')
'''

# Register your models here.
admin.site.register(User)
admin.site.register(Settings, SettingsAdmin)
# admin.site.register(Team, TeamAdmin)
