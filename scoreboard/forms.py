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
        options = {
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
            "lib_aceeditor": 0,
            "lib_autocomplete": 0,
            "lib_sceditor": 0,
            "lib_simplemde": 0,
            "lib_select2": 0,
            "lib_selectize": 0,
            "lib_choices": 0,
            "lib_flatpickr": 0,
            "lib_signaturepad": 0,
            "lib_mathjs": 0,
            "lib_cleavejs": 0,
            "lib_jodit": 0,
            "lib_jquery": 1,
            "lib_dompurify": 0
        },
        ajax = False
    )