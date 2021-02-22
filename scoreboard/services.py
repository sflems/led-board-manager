from django.conf import settings
from django.http import Http404
import json, psutil, requests, subprocess
from gpiozero import CPUTemperature
from .models import *

# Supervisor Commands for NHL Led Scoreboard
def proc_status():
    proc_status = False
    command = "sudo supervisorctl status scoreboard"
    process = subprocess.run(command, shell=True, capture_output=True)

    # Checks if bytes type string RUNNING is found in output(bytes type).
    if b'RUNNING' in process.stdout:
        proc_status = True

    return proc_status

# Pi System Stats Functions
# Imported from https://learn.pimoroni.com/tutorial/networked-pi/raspberry-pi-system-stats-python and modified for this use case.
def cpu():
    return str(psutil.cpu_percent()) + '%'

def cputemp():
    return str(CPUTemperature().temperature) + '&deg;C'

def memory():
    memory = psutil.virtual_memory()
    # Divide from Bytes -> KB -> MB
    available = round(memory.available/1024.0/1024.0,1)
    total = round(memory.total/1024.0/1024.0,1)
    return str(available) + 'MB free / ' + str(total) + 'MB total (' + str(memory.percent) + '%)'

def disk():
    disk = psutil.disk_usage('/')
    # Divide from Bytes -> KB -> MB -> GB
    free = round(disk.free/1024.0/1024.0/1024.0,1)
    total = round(disk.total/1024.0/1024.0/1024.0,1)
    return str(free) + 'GB free / ' + str(total) + 'GB total (' + str(disk.percent) + '%)'

# NHL API Functions
# Gets the team abbreviation by id from the NHL API.
def team_abbrev(id):
    url = 'https://statsapi.web.nhl.com/api/v1/teams' + id
    response = requests.get(url)
    team = response.json()
    return team

# Gets todays games from the NHL API.        
def todays_games():
    url = 'https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.linescore'
    response = requests.get(url)
    games = response.json()
    games = games['dates'][0]['games']
    return games

# defines the users home/user/nhl-led-scoreboard/config folder path. Checks if DEMO_CS50 mode is enabled.
def conf_path():
    return path

# Opens default config from current config in the nhl-led-scoreboard folder if found, otherwise from static config, and then loads into Settings Profile
def conf_default():
    with open(os.path.join(settings.BASE_DIR, "scoreboard/static/schema/config.json"), "r") as f:
        conf = json.load(f)
        return conf

# Defines config schema used by the current led-scoreboard version. File is opened, converted from binary to a python/django object and then used as a callable object.
def schema():
    try:
        with open(conf_path() + "config.schema.json", "r") as f:
            conf = json.load(f)
            return conf
    except:
        raise Http404("Schema does not exist.")

# Options for JSON created settings form.
# startval takes in current settings (NOT VALIDATED AGAINST SCHEMA). Others modify which JSON editing options are visible to users, themes, etc.
def form_options(startval):
    options = {
            "startval": startval,
            "theme": "bootstrap4",
            "object_layout": "default",
            "template": "default",
            "show_errors": "interaction",
            "required_by_default": 0,
            "no_additional_properties": 1,
            "display_required_only": 0,
            "remove_empty_properties": 0,
            "keep_oneof_values": 0,
            "ajax": 1,
            "ajaxCredentials": 0,
            "show_opt_in": 0,
            "disable_edit_json": 1,
            "disable_collapse": 0,
            "disable_properties": 1,
            "disable_array_add": 0,
            "disable_array_reorder": 0,
            "disable_array_delete": 0,
            "enable_array_copy": 0,
            "array_controls_top": 1,
            "disable_array_delete_all_rows": 1,
            "disable_array_delete_last_row": 1,
            "prompt_before_delete": 1,
        }
    return options
