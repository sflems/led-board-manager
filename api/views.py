from django.shortcuts import render
from rest_framework import viewsets, permissions
from scoreboard.models import Settings, Team
from .serializers import SettingsSerializer, TeamSerializer

# Create your views here.
class SettingsView(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

class TeamView(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
