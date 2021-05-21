from django.shortcuts import render
from rest_framework import viewsets, permissions
from scoreboard.models import Settings, BoardType, Team
from .serializers import SettingsSerializer, BoardTypeSerializer, TeamSerializer

# Create your views here.
class SettingsView(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

class BoardTypeView(viewsets.ModelViewSet):
    queryset = BoardType.objects.all()
    serializer_class = BoardTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)

class TeamView(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (permissions.AllowAny,)
