from django.test import TestCase
from constance.test import override_config
from scoreboard.services import gui_status, form_options


# Test Various GUI Functions
@override_config(SUPERVISOR_GUI_NAME="testing")
class ServicesTests(TestCase):
    # Tests if gui supervisor status is 'RUNNING'.
    def test_gui_status(self):
        self.assertFalse(gui_status())

    # Tests if object passed to form_options() is added and returned correctly.
    def test_form_options(self):
        test_dict = {
            "startval": {"test": "value"},
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
            "disable_edit_json": 1,
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
        self.assertDictEqual(form_options({"test": "value"}), test_dict)
