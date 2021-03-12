import os
from update_check import isUpToDate
from django.conf import settings


# This is a context processor to add custom {{ variables }} to templates.
def version(request):
    path = os.path.join(settings.BASE_DIR, "VERSION")
    update = not isUpToDate(
        path,
        'https://raw.githubusercontent.com/sflems/nhl-led-scoreboard-webgui/main/VERSION'
    )
    version = settings.VERSION
    # Return the value you want as a dictionnary. You may add multiple values in here.
    return {'VERSION': version, 'UPDATE': update}

# Update Check for use in context processor
