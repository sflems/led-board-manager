from rest_framework import serializers
from scoreboard.models import Settings

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'url', 'name', 'config', 'isActive',]