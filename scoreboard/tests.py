from constance import config
from constance.test import override_config
from django.test import Client, TestCase, override_settings
import os, pytz, unittest
from django.conf import settings
from scoreboard.services import conf_path, conf_default, schema
from scoreboard.models import Settings

# Test Various GUI Functions
class Tests(unittest.TestCase):

    def test_valid_pi_tz(self):
        tz = settings.TIME_ZONE
        valid_tzs = pytz.common_timezones
        self.assertIn(tz, valid_tzs)

   # Checks conf_path() base on constance path configuration.
    @override_config(SCOREBOARD_DIR=os.path.join(config.GUI_DIR, "testing"))    
    def test_conf_path_exists(self):
        path = conf_path()
        self.assertIsNotNone(path)

    # Tests that schema() returns based on constance path configuration.
    @override_config(SCOREBOARD_DIR=os.path.join(config.GUI_DIR, "testing"))
    def test_get_schema(self):
        self.assertIsNotNone(schema())


# Test Server Responses
class SimpleTest(TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertRedirects(response, '/login?next=/')

    def test_default_login(self):
        client = Client()
        response = client.get('/login?next=/')
        self.assertEqual(response.status_code, 200)

# Settings Model / Config Tests
@override_settings(TEST_MODE=True)
@override_config(SCOREBOARD_DIR=os.path.join(config.GUI_DIR, "testing"))
class SettingsTestCase(TestCase):

    # Setup Testing Settings instances.
    def setUp(self):
            Settings.objects.create(name="Test Profile", config=conf_default(), isActive=True)
            Settings.objects.create(name="Test Profile2", config=conf_default(), isActive=False)
        
    def test_backup_save(self):
            p1 = Settings.objects.get(name="Test Profile").save_to_file()
            self.assertTrue(os.path.isfile(p1))
 
   # Removes created test files.
    def tearDown(self):
        if os.path.isfile(os.path.join(config.GUI_DIR, "testing/config/test-profile.config.json")):
            os.remove("testing/config/config.json")

        if os.path.isfile(os.path.join(config.GUI_DIR, "testing/config/test-profile.config.json")):
            os.remove("testing/config/test-profile.config.json")
            
'''
    def test_valid_config(self):
        # For properties in config, validated against properties from schema.j
        # ...Or use fastjsonschema
'''
    

