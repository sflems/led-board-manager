from django.apps import AppConfig
from constance.apps import ConstanceConfig

class CustomConstance(ConstanceConfig):
    verbose_name = "Settings"

class ScoreboardConfig(AppConfig):
    name = 'scoreboard'
