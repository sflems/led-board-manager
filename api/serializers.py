from rest_framework import serializers
from scoreboard.models import Settings, BoardType, Team

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'url', 'name', 'boardType', 'isActive', 'config']

class BoardTypeSerializer(serializers.ModelSerializer):

    activeConfig = serializers.JSONField(source='configJSON', read_only=True)
    
    class Meta:
        model = BoardType
        fields = ['board', 'path', 'supervisorName', 'activeConfig', 'schema']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'abbreviation', 'teamName', 'locationName', 'jsonLink', 'officialSiteUrl']
