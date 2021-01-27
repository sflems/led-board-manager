from django.forms import ModelForm, Form
from django_jsonforms.forms import JSONSchemaField
from .models import Settings
import json

# TO DO: Document usage of django-jsonforms

# Defines config schema used by the current led-scoreboard version. File is opened, converted from binery to a python/django object and then used as a callable object.
def schema():
    with open("./scoreboard/static/schema/config.schema.json", "r") as f:
        conf = json.load(f)
        return conf
schema = schema()

# Gets the active config to later instantiate SettingsForm
current_conf = Settings.objects.filter(isActive=1).first().config

# This is the django-jsonforms implementation for the scoreboard config. It generates a form based on the current schema config and populates with with the active config.
class SettingsForm(Form):
    json = JSONSchemaField(

        # Default config schema to be used
        schema = schema,

        # Options for JSON created settings form.
        # startval takes in current settings as long as they are schema valid. Others modify which JSON editing options are visible to users, themes, etc.
        options = {
            "startval": current_conf, 
            "theme": "bootstrap4",
            "iconlib": "none",
            "object_layout": "grid",
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
            "lib_jquery": 1,
            "collapsed": 1
        },

        # TO DO! Define me.
        ajax = True
    )
