from django.test import TestCase
import unittest, pytz

from Capstone.settings import pi_tz

class Tests(unittest.TestCase):
    def test_pi_tz(self):
        tz = pi_tz()
        valid_tzs = pytz.all_timezones
        self.assertIn(tz, valid_tzs)