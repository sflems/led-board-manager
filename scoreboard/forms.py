from django.forms import ModelForm, Form
from django_jsonforms.forms import JSONSchemaField
import json

# TO DO: Document usage of django-jsonforms

def schema():
    with open("./scoreboard/static/schema/config.schema.json", "r") as f:
        conf = json.load(f)
        return conf

schema = schema()

class SettingsForm(Form):
    json = JSONSchemaField(
        schema = schema,
        options = {"theme": "bootstrap3", "no_additional_properties": True, "disable_properties": True},
        ajax = False
    )