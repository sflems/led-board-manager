import json, os, pytz, unittest
from django.test import Client, TestCase, override_settings
from django.conf import settings
from constance import config
from constance.test import override_config
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

    # TO DO: Add test for conf_default() here.

    # Tests that schema() returns based on constance path configuration.
    @override_config(SCOREBOARD_DIR=os.path.join(config.GUI_DIR, "testing"))
    def test_get_schema(self):
        self.assertIsNotNone(schema())


# Test Server Responses
class SimpleTest(TestCase):
    def test_index_redirect(self):
        client = Client()
        response = client.get('/')
        self.assertRedirects(response, '/login?next=/')

    def test_login_page(self):
        client = Client()
        response = client.get('/login?next=/')
        self.assertEqual(response.status_code, 200)

    def test_default_login(self):
        client = Client()
        response = client.post('/login?next=/', {'username': 'admin', 'password': 'scoreboard'})
        self.assertEqual(response.status_code, 200)

# Settings Model / Config Tests
@override_settings(TEST_MODE=True)
@override_config(SCOREBOARD_DIR=os.path.join(config.GUI_DIR, "testing"))
class SettingsTestCase(TestCase):

    # Dummy Confs used in setUp().
    def conf1(self):
        with open(os.path.join(config.GUI_DIR, "scoreboard/static/schema/config.json.sample"), "r") as f:
            conf = json.load(f)
            return conf

    # Dummy Confs used in setUp().
    conf2 = json.loads('{"debug":false,"loglevel":"INFO","live_mode":true,"preferences":{"time_format":"12h","end_of_day":"00:00","location":"CAMPBELL RIVER, BC","live_game_refresh_rate":10,"teams":["Maple Leafs","Golden Knights"],"sog_display_frequency":4,"goal_animations":{"pref_team_only":false}},"states":{"off_day":["scoreticker","standings","clock","weather"],"scheduled":["standings","scoreticker"],"intermission":["scoreticker","team_summary","clock"],"post_game":["standings","scoreticker","clock","weather"]},"boards":{"scoreticker":{"preferred_teams_only":false,"rotation_rate":5},"seriesticker":{"preferred_teams_only":true,"rotation_rate":5},"standings":{"preferred_standings_only":true,"standing_type":"conference","divisions":"north","conference":"western"},"clock":{"duration":15,"hide_indicator":false,"preferred_team_colors":true,"clock_rgb":"","date_rgb":"","flash_seconds":false},"covid19":{"worldwide_enabled":false,"country_enabled":false,"country":["USA"],"us_state_enabled":false,"us_state":["New York"],"canada_enabled":false,"canada_prov":["Quebec"]},"weather":{"enabled":true,"view":"full","units":"metric","duration":30,"data_feed":"EC","owm_apikey":"","update_freq":15,"show_on_clock":true,"forecast_enabled":true,"forecast_days":2,"forecast_update":1},"wxalert":{"alert_feed":"EC","update_freq":5,"nws_show_expire":false,"show_alerts":true,"alert_title":true,"scroll_alert":true,"alert_duration":5,"show_on_clock":true}},"sbio":{"screensaver":{"enabled":true,"animations":true,"start":"01:00","stop":"17:00","data_updates":false,"motionsensor":true,"pin":24,"delay":30},"dimmer":{"enabled":false,"source":"software","frequency":5,"light_level_lux":400,"mode":"always","daytime":"","nighttime":"","offset":90,"sunset_brightness":5,"sunrise_brightness":40},"pushbutton":{"enabled":false,"bonnet":false,"pin":25,"reboot_duration":2,"reboot_override_process":"","display_reboot":true,"poweroff_duration":10,"poweroff_override_process":"","display_halt":true,"state_triggered1":"weather","state_triggered1_process":""}}}')
    conf3 = json.loads('{"debug":false,"loglevel":"INFO","live_mode":true,"preferences":{"time_format":"12h","end_of_day":"8:00","location":"","live_game_refresh_rate":10,"teams":["Canadiens"],"sog_display_frequency":4,"goal_animations":{"pref_team_only":true}},"states":{"off_day":["scoreticker","standings","team_summary","clock"],"scheduled":["standings","team_summary","scoreticker","clock"],"intermission":["scoreticker","team_summary"],"post_game":["standings","team_summary","scoreticker","clock"]},"boards":{"scoreticker":{"preferred_teams_only":false,"rotation_rate":5},"seriesticker":{"preferred_teams_only":true,"rotation_rate":5},"standings":{"preferred_standings_only":true,"standing_type":"wild_card","divisions":"north","conference":"eastern"},"clock":{"duration":15,"hide_indicator":false,"preferred_team_colors":true,"clock_rgb":"","date_rgb":"","flash_seconds":true},"covid19":{"worldwide_enabled":false,"country_enabled":false,"country":["USA"],"us_state_enabled":false,"us_state":["New York"],"canada_enabled":false,"canada_prov":["Quebec"]},"weather":{"enabled":false,"view":"full","units":"metric","duration":60,"data_feed":"EC","owm_apikey":"","update_freq":5,"show_on_clock":true,"forecast_enabled":false,"forecast_days":3,"forecast_update":1},"wxalert":{"alert_feed":"EC","update_freq":5,"show_alerts":false,"nws_show_expire":false,"alert_title":true,"scroll_alert":true,"alert_duration":5,"show_on_clock":true}},"sbio":{"screensaver":{"enabled":false,"animations":true,"start":"22:00","stop":"08:00","data_updates":false,"motionsensor":false,"pin":7,"delay":30},"dimmer":{"enabled":false,"source":"software","daytime":"","nighttime":"","offset":0,"frequency":5,"light_level_lux":400,"mode":"always","sunset_brightness":5,"sunrise_brightness":40},"pushbutton":{"enabled":false,"bonnet":false,"pin":25,"reboot_duration":2,"reboot_override_process":"","display_reboot":true,"poweroff_duration":10,"poweroff_override_process":"","display_halt":true,"state_triggered1":"weather","state_triggered1_process":""}}}')

    # Setup Testing Settings instances.
    def setUp(self):

        # Default Config Provided with services.conf_default() function.
        Settings.objects.create(name="Test Profile1", config=conf_default(), isActive=True)
        # Sample Config Provided with GUI
        Settings.objects.create(name="Test Profile2", config=self.conf1(), isActive=True)
        # Dummy confs)
        Settings.objects.create(name="Test Profile3", config=self.conf2, isActive=False)
        Settings.objects.create(name="Test Profile4", config=self.conf3, isActive=True)
        
    @unittest.expectedFailure
    def test_config_cannot_be_null(self):
        Settings.objects.create(name="Test Profile5", isActive=True)
        self.fail('Settings.config cannot be none.')
  
    @unittest.expectedFailure
    def test_config_cannot_be_empty(self):
        Settings.objects.create(name="Test Profile6", config="", isActive=True)
        self.fail('Settings.config cannot be empty string')
        
    # Confirm the following actions based on test setup. Checks custom GUI model logic.
    def test_count_settings(self):
        self.assertEqual(Settings.objects.all().count(), 4)

    def test_count_active(self):
        self.assertEqual(Settings.objects.filter(isActive=1).count(), 1)

    def test_backup_save(self):
        p1 = Settings.objects.get(name="Test Profile1").save_to_file()
        self.assertTrue(os.path.isfile(p1))

    # Removes created test files.
    def tearDown(self):
        if os.path.isfile(os.path.join(config.GUI_DIR, "testing/config/config.json")):
            os.remove("testing/config/config.json")

        if os.path.isfile(os.path.join(config.GUI_DIR, "testing/config/test-profile1.config.json")):
            os.remove("testing/config/test-profile1.config.json")
