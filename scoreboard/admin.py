from django.contrib import admin
from .models import Settings, Team, User
from .forms import SettingsDetailForm, SettingsJSONForm

# TO DO: Change default admin form to JSONForm
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'isActive')
    list_display_links = ('id', 'name',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'teamName', 'abbreviation',)
    ordering = ('teamName',)
    readonly_fields = ('name', 'abbreviation', 'teamName', 'locationName', 'jsonLink', 'officialSiteUrl')

# Register your models here.
admin.site.register(User)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Team, TeamAdmin)
