from django.contrib import admin
from .models import Settings, Team, User

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'teamName', 'abbreviation',)
    ordering = ('teamName',)

# Register your models here.
admin.site.register(User)
admin.site.register(Settings)
admin.site.register(Team, TeamAdmin)
