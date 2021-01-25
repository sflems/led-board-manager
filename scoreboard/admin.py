from django.contrib import admin
from .models import Team, User

# Register your models here.
admin.site.register(User)
admin.site.register(Team)