import requests
import json
from .models import *

# Gets the users home folder and then the nhl-led-scoreboard folder.
def install_path():
    path = os.path.expanduser("~") + "/nhl-led-scoreboard/config"
    return path

# Opens default config from model object if found, otherwise from file, and then loads into Settings Profile
def conf_default():
        try:
            conf = Settings.objects.get(name__iexact="default").config
            return conf
        except:
            path = install_path() + "/config.json.sample"
            with open(path, "r") as f:
                conf = json.load(f)
                return conf
                
def todays_games():
    url = 'https://statsapi.web.nhl.com/api/v1/schedule'
    response = requests.get(url)
    games = response.json()
    return games['dates'][0]['games']

# Defines config schema used by the current led-scoreboard version. File is opened, converted from binery to a python/django object and then used as a callable object.
def schema():
    with open("./scoreboard/static/schema/config.schema.json", "r") as f:
        conf = json.load(f)
        return conf

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
            "disable_edit_json": 0,
            "disable_collapse": 0,
            "disable_properties": 1,
            "disable_array_add": 0,
            "disable_array_reorder": 0,
            "disable_array_delete": 0,
            "enable_array_copy": 0,
            "array_controls_top": 1,
            "disable_array_delete_all_rows": 0,
            "disable_array_delete_last_row": 0,
            "prompt_before_delete": 1,
        }
    return options