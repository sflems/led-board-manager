import json, os, pytz, unittest
from django.test import Client, TestCase, override_settings
from django.conf import settings
from scoreboard.models import Settings, BoardType


# Test Various GUI Functions
class Tests(unittest.TestCase):
    def test_valid_pi_tz(self):
        tz = settings.TIME_ZONE
        valid_tzs = pytz.common_timezones
        self.assertIn(tz, valid_tzs)

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

    def test_context(self):
        client = Client()
        response = client.post('/login?next=/', {'username': 'admin', 'password': 'scoreboard'})
        self.assertListEqual(response.context['BOARDS'], [])
        self.assertRegex(response.context['VERSION'], r'^v[0-9]+.[0-9]+.[0-9]+$')
        self.assertIsNotNone(response.context['UPDATE'])

# Settings Model / Config Tests
@override_settings(TEST_MODE=True)
class SettingsTestCase(TestCase):

    # Dummy Confs used in setUp().
    def conf1(self):
        with open(os.path.join(settings.BASE_DIR, "scoreboard/static/schema/config.json.sample"), "r") as f:
            conf = json.load(f)
            return conf

    # Dummy Confs used in setUp().
    conf2 = json.loads('{"debug":false,"loglevel":"INFO","live_mode":true,"preferences":{"time_format":"12h","end_of_day":"00:00","location":"CAMPBELL RIVER, BC","live_game_refresh_rate":10,"teams":["Maple Leafs","Golden Knights"],"sog_display_frequency":4,"goal_animations":{"pref_team_only":false}},"states":{"off_day":["scoreticker","standings","clock","weather"],"scheduled":["standings","scoreticker"],"intermission":["scoreticker","team_summary","clock"],"post_game":["standings","scoreticker","clock","weather"]},"boards":{"scoreticker":{"preferred_teams_only":false,"rotation_rate":5},"seriesticker":{"preferred_teams_only":true,"rotation_rate":5},"standings":{"preferred_standings_only":true,"standing_type":"conference","divisions":"north","conference":"western"},"clock":{"duration":15,"hide_indicator":false,"preferred_team_colors":true,"clock_rgb":"","date_rgb":"","flash_seconds":false},"covid19":{"worldwide_enabled":false,"country_enabled":false,"country":["USA"],"us_state_enabled":false,"us_state":["New York"],"canada_enabled":false,"canada_prov":["Quebec"]},"weather":{"enabled":true,"view":"full","units":"metric","duration":30,"data_feed":"EC","owm_apikey":"","update_freq":15,"show_on_clock":true,"forecast_enabled":true,"forecast_days":2,"forecast_update":1},"wxalert":{"alert_feed":"EC","update_freq":5,"nws_show_expire":false,"show_alerts":true,"alert_title":true,"scroll_alert":true,"alert_duration":5,"show_on_clock":true}},"sbio":{"screensaver":{"enabled":true,"animations":true,"start":"01:00","stop":"17:00","data_updates":false,"motionsensor":true,"pin":24,"delay":30},"dimmer":{"enabled":false,"source":"software","frequency":5,"light_level_lux":400,"mode":"always","daytime":"","nighttime":"","offset":90,"sunset_brightness":5,"sunrise_brightness":40},"pushbutton":{"enabled":false,"bonnet":false,"pin":25,"reboot_duration":2,"reboot_override_process":"","display_reboot":true,"poweroff_duration":10,"poweroff_override_process":"","display_halt":true,"state_triggered1":"weather","state_triggered1_process":""}}}')
    conf3 = json.loads('{"debug":true,"loglevel":"WARNING","live_mode":false,"preferences":{"time_format":"12h","end_of_day":"8:00","location":"","live_game_refresh_rate":10,"teams":["Canadiens"],"sog_display_frequency":4,"goal_animations":{"pref_team_only":true}},"states":{"off_day":["scoreticker","standings","team_summary","clock"],"scheduled":["standings","team_summary","scoreticker","clock"],"intermission":["scoreticker","team_summary"],"post_game":["standings","team_summary","scoreticker","clock"]},"boards":{"scoreticker":{"preferred_teams_only":false,"rotation_rate":5},"seriesticker":{"preferred_teams_only":true,"rotation_rate":5},"standings":{"preferred_standings_only":true,"standing_type":"wild_card","divisions":"north","conference":"eastern"},"clock":{"duration":15,"hide_indicator":false,"preferred_team_colors":true,"clock_rgb":"","date_rgb":"","flash_seconds":true},"covid19":{"worldwide_enabled":false,"country_enabled":false,"country":["USA"],"us_state_enabled":false,"us_state":["New York"],"canada_enabled":false,"canada_prov":["Quebec"]},"weather":{"enabled":false,"view":"full","units":"metric","duration":60,"data_feed":"EC","owm_apikey":"","update_freq":5,"show_on_clock":true,"forecast_enabled":false,"forecast_days":3,"forecast_update":1},"wxalert":{"alert_feed":"EC","update_freq":5,"show_alerts":false,"nws_show_expire":false,"alert_title":true,"scroll_alert":true,"alert_duration":5,"show_on_clock":true}},"sbio":{"screensaver":{"enabled":false,"animations":true,"start":"22:00","stop":"08:00","data_updates":false,"motionsensor":false,"pin":7,"delay":30},"dimmer":{"enabled":false,"source":"software","daytime":"","nighttime":"","offset":0,"frequency":5,"light_level_lux":400,"mode":"always","sunset_brightness":5,"sunrise_brightness":40},"pushbutton":{"enabled":false,"bonnet":false,"pin":25,"reboot_duration":2,"reboot_override_process":"","display_reboot":true,"poweroff_duration":10,"poweroff_override_process":"","display_halt":true,"state_triggered1":"weather","state_triggered1_process":""}}}')

    # Setup Testing Settings instances.
    def setUp(self):

        # Creates initial NHL board for testing
        BoardType.objects.create(
            pk='NHL',
            path=os.path.join(settings.BASE_DIR, "testing"),
            supervisorName="NHLscoreboard"
        )
        BoardType.objects.create(
            pk='NHL2',
            path=os.path.join(settings.BASE_DIR, "testing", "config"),
            supervisorName="NHLscoreboard2"
        )

        # Sample Config Provided with GUI
        Settings.objects.create(name="Test Profile2", config=self.conf1(), isActive=True)
        # Dummy confs)
        Settings.objects.create(pk=3, boardType=BoardType.objects.get(
            pk='NHL2'), name="Test Profile3", config=self.conf2, isActive=False)
        Settings.objects.create(pk=4, name="Test Profile4", config=self.conf3, isActive=True)

    def test_board_type(self):
        bt = BoardType.objects.get(pk='NHL')
        self.assertEqual(bt.path, os.path.join(settings.BASE_DIR, "testing"))
        self.assertEqual(bt.pythonVersion, '3')
        self.assertEqual(bt.supervisorName, "NHLscoreboard")

    def test_board_type_conf_dir(self):
        self.assertIn("led-board-manager/testing/config", BoardType.objects.get(pk='NHL').conf_dir())

    def test_board_type_main(self):
        self.assertEqual("./main.py", BoardType.objects.get(pk='NHL').main())
        self.assertEqual("./src/main.py", BoardType.objects.get(pk='NHL2').main())

    def test_board_type_schema(self):
        bt = BoardType.objects.get(pk='NHL').schema()
        self.assertEqual(bt['title'], "NHL LED Scoreboard configuration")
        self.assertEqual(bt['properties']['debug']['title'], "debug")

    def test_board_type_configJSON(self):
        p = Settings.objects.get(name='Test Profile4')
        bt = BoardType.objects.get(pk='NHL')
        self.assertEqual(p.config, bt.configJSON())

    def test_board_type_str(self):
        self.assertEqual(BoardType.objects.get(pk="NHL").__str__(), "NHL")

    # Confirm the following actions based on test setup. Checks custom GUI model logic.
    def test_count_settings(self):
        self.assertEqual(Settings.objects.all().count(), 3)

    def test_settings_str(self):
        self.assertEqual(Settings.objects.get(pk=4).__str__(), "Test Profile4 Profile")

    def test_count_active(self):
        self.assertEqual(Settings.objects.filter(isActive=1).count(), 1)

    def test_backup_save(self):
        p1 = Settings.objects.get(name="Test Profile2").save_to_file()
        self.assertTrue(os.path.isfile(p1))

    # Removes created test files.
    def tearDown(self):
        if os.path.isfile(os.path.join(settings.BASE_DIR, "testing/config/config.json")):
            os.remove("testing/config/config.json")

        if os.path.isfile(os.path.join(settings.BASE_DIR, "testing/config/Test-Profile2.config.json")):
            os.remove("testing/config/Test-Profile2.config.json")
