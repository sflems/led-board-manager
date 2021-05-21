from rest_framework import serializers
from scoreboard.models import Settings, BoardType, Team

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'url', 'name', 'boardType', 'isActive', 'config']

class BoardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardType
        fields = ['board', 'path', 'supervisorName',]

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'abbreviation', 'teamName', 'locationName', 'jsonLink', 'officialSiteUrl']