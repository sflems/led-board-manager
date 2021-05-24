from django import forms

# This Settings mo# This Settings model form gets the name and isActive attributes from the user.
class SettingsDetailForm(forms.Form):
    name = forms.CharField(max_length=32, label="Profile Name:")
    isActive = forms.BooleanField(required=False, label="Make this the active profile?")
