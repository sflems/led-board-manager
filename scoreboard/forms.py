from django import forms
from django_jsonforms.forms import JSONSchemaField
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .services import *
import json

# Gets the active config, or default if not found, to later instantiate SettingsForm.
try:
    current_conf = Settings.objects.get(isActive=1).config
except:
    current_conf = conf_default()

schema = schema()
options = form_options(current_conf)

# django-jsonforms implementation for the scoreboard config. It generates a form based on the current config schema and populates with with the active config settings in the json attribute.
class SettingsJSONForm(forms.Form):
    json = JSONSchemaField(schema=schema, options=options, ajax=True)
    class Meta:
        labes = {
             "json":"",
        }

# This Settings mo# This Settings model form gets the name and isActive attributes from the user.
class SettingsDetailForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('name', 'isActive')
        labels = {
            "name": "Profile Name",
            "isActive": "Make this the active profile?"
        }
        