
import json, os, psutil, requests, subprocess
from gpiozero import CPUTemperature
from django import template
from django.utils.formats import localize
from django.http import Http404
from django.dispatch import receiver
from django.conf import settings
from constance import config
from constance import settings as configsettings
from constance.signals import admin_form_save

from scoreboard.models import BoardType
from sh import git

# Supervisor Commands for NHL Led Scoreboard
def gui_status():
    proc_status = False
    command = "sudo supervisorctl status " + config.SUPERVISOR_GUI_NAME
    process = subprocess.run(command, shell=True, capture_output=True)

    # Checks if bytes type string RUNNING is found in output(bytes type).
    if b'RUNNING' in process.stdout:
        proc_status = True

    return proc_status

# defines the users home/user/nhl-led-scoreboard/config folder path.
def conf_path():
    path = os.path.join(config.SCOREBOARD_DIR, 'config/')
    if settings.TEST_MODE == True:
        return os.path.join(config.GUI_DIR, 'testing', 'config/')
    elif not os.path.isdir(path):
        error = "Scoreboard config directory not found. Check SCOREBOARD_DIR (path) configuration in Admin Panel. Configured path: \"" + path + "\""
        raise ValueError(error)
    else:
        return path

# Opens default config from current config in the nhl-led-scoreboard folder if found, otherwise from static config, and then loads into Settings Profile
# TRY TO GET DEFAULT FROM SCOREBOARD .default DIR, then fallback.
def conf_default():
    config_file = os.path.join(conf_path(), ".default", "config.json.sample")
    if not os.path.exists(config_file):
        config_file = os.path.join(config.GUI_DIR, "scoreboard/static/schema/config.json")
    with open(config_file, "r") as f:
        conf = json.load(f)
        return conf


# Defines config schema used by the current led-scoreboard version.
# File is opened, converted from binary to a python/django object and then used as a callable object.
def schema():
    try:
        path = os.path.join(conf_path(), "config.schema.json")

        if not os.path.isfile(path):
            path = os.path.join(config.GUI_DIR, "scoreboard/static/schema/config.schema.json")

        with open(path, "r") as f:
            conf = json.load(f)
            return conf
    except FileNotFoundError:
        raise Http404("\"config.schema.json\" not found. Check SCOREBOARD_DIR (path) configuration in Admin Panel. Configured path: \"" + conf_path() + "\"")

# Options for JSON created settings form.
# startval takes in current settings (NOT VALIDATED AGAINST SCHEMA). Others modify which JSON editing options are visible to users, themes, etc.
def form_options(startval):
    options = {
        "startval": startval,
        "theme": "bootstrap4",
        "object_layout": "grid",
        "template": "default",
        "show_errors": "interaction",
        "required_by_default": 0,
        "no_additional_properties": 1,
        "display_required_only": 0,
        "remove_empty_properties": 0,
        "keep_oneof_values": 0,
        "ajax": 0,
        "ajaxCredentials": 0,
        "show_opt_in": 0,
        "disable_edit_json": 0,
        "disable_collapse": 0,
        "disable_properties": 1,
        "disable_array_add": 0,
        "disable_array_reorder": 0,
        "disable_array_delete": 0,
        "enable_array_copy": 1,
        "array_controls_top": 1,
        "disable_array_delete_all_rows": 1,
        "disable_array_delete_last_row": 1,
        "prompt_before_delete": 1,
    }
    return options

# The below functions render the supervisor config file with django template logic to allow constance variables.
# Taken from  deprecated django-supervisor pypi module. See https://github.com/rfk/django-supervisor for reference.
def render_sv_config(data, ctx):
    """Render the given config data using Django's template system.
    This function takes a config data string and a dict of context variables,
    renders the data through Django's template system, and returns the result.
    """
    t = template.Template(data)
    c = template.Context(ctx)
    return t.render(c).encode("ascii")

# Listens for Constance settings update. If signal rcv'd, the below functions run to update supervisor-daemon.conf and reload.
@receiver(admin_form_save)
def constance_updated(sender, **kwargs):
    # Update supervisor confs
    command = "sudo supervisorctl update"
    return sv_template(), subprocess.run(command, shell=True)

def sv_template():
    # Interpret paths relative to the project directory.
    path = os.path.join(config.GUI_DIR, 'scoreboard/templates/scoreboard/daemon-template.conf')
    templated_path = os.path.join(config.GUI_DIR, 'supervisor-daemon.conf')

    # Read and process the source file. Import flags from constance and save to supervisor config.
    flags = []
    flag_fields = configsettings.CONFIG_FIELDSETS['Scoreboard Flags']['fields']
    for flag in flag_fields:
        key = flag.lower().replace('_', '-')
        default = configsettings.CONFIG[str(flag)][0]
        value = str(getattr(config, flag))
        default_args = ["led-brightness", "led-gpio-mapping", "led-slowdown-gpio", "led-rows", "led-cols", "updatecheck", ]
        basic_args = ["led-show-refresh", "updatecheck", ]

        def is_modified():
            return localize(value) != localize(default)

        def render_flag():
            if key in basic_args and value == "True":
                full_flag = " --" + key
                flags.append(full_flag)
            elif key in basic_args:
                full_flag = ""
                flags.append(full_flag)
            else:
                full_flag = " --" + key + "=" + value
                flags.append(full_flag)

        if key in default_args:
            render_flag()

        elif is_modified():
            render_flag()

    # Add optional board args here to convert to flags.
    boards = BoardType.objects.all()
    boardsList = []
    for board in BoardType.objects.all():
        boardsList.append(board.supervisorName)

    # Renders from daemon template with config and flags passed in as context.
    with open(path, "r") as f:
        templated = render_sv_config(f.read(), {'config': config, 'flags': flags, 'boards': boards, 'boardslist': boardsList })

    # Write it out to the corresponding .conf file.
    with open(templated_path, "w") as f:
        f.write(str(templated, 'utf-8'))

    # Copy metadata if necessary.
    return templated_path

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

# Pi System Stats Functions
# Imported from https://learn.pimoroni.com/tutorial/networked-pi/raspberry-pi-system-stats-python and modified for this use case.
def cpu():
    return str(psutil.cpu_percent()) + '%'

def cputemp():
    return str(CPUTemperature().temperature) + '&deg;C'

def memory():
    memory = psutil.virtual_memory()
    # Divide from Bytes -> KB -> MB
    available = round(memory.available/1024.0/1024.0, 1)
    total = round(memory.total/1024.0/1024.0, 1)
    return str(available) + 'MB free / ' + str(total) + 'MB total (' + str(memory.percent) + '%)'

def disk():
    disk = psutil.disk_usage('/')
    # Divide from Bytes -> KB -> MB -> GB
    free = round(disk.free/1024.0/1024.0/1024.0, 1)
    total = round(disk.total/1024.0/1024.0/1024.0, 1)
    return str(free) + 'GB free / ' + str(total) + 'GB total (' + str(disk.percent) + '%)'
