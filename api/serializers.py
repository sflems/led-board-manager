from rest_framework import serializers
from scoreboard.models import Settings, Team

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'url', 'name', 'config', 'isActive']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'abbreviation', 'teamName', 'locationName', 'jsonLink', 'officialSiteUrl']