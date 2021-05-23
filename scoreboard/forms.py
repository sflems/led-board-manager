from django import forms
from .models import Settings

# This Settings mo# This Settings model form gets the name and isActive attributes from the user.
class SettingsDetailForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('name', 'isActive')
        labels = {
            "name": "Profile Name:",
            "isActive": "Make this the active profile?"
        }
    
