from django.shortcuts import render
from rest_framework import viewsets, permissions
from scoreboard.models import Settings
from .serializers import SettingsSerializer

# Create your views here.
class SettingsView(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)