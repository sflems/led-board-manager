from django.test import Client, TestCase
import os, pytz, unittest

from Capstone.settings import pi_tz
from scoreboard.services import conf_path, conf_default, schema
from scoreboard.models import Settings

class Tests(unittest.TestCase):

    def test_valid_pi_tz(self):
        tz = pi_tz()
        valid_tzs = pytz.all_timezones
        self.assertIn(tz, valid_tzs)
    
    def test_conf_path_exists(self):
        path = conf_path()
        self.assertIsNotNone(path)

    # Expand schema validation tests here
    def test_schema_exists(self):
        self.assertIsNotNone(schema())

"""
class SettingsTestCase(TestCase):

    # Sample Data
    def SetUp(self):
        Settings.objects.create(name="Test Profile", config=conf_default(), isActive=True)
        Settings.objects.create(name="Test Profile2", config=conf_default(), isActive=False)
"""
