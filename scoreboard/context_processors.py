import os
from update_check import isUpToDate
from django.conf import settings
from .models import BoardType


# This is a context processor to add custom {{ variables }} to templates.
# Update Check for use in context processor
def version(request):
    #Gets path to local version file.
    path = os.path.join(settings.BASE_DIR, "VERSION")

    # Checks local version file against current release version
    update = not isUpToDate(
        path,
        'https://raw.githubusercontent.com/sflems/nhl-led-scoreboard-webgui/main/VERSION'
    )

    # Sets version for context.
    version = settings.VERSION

    # Adds available boards for use in context/templates.
    boards = []
    for board in BoardType.objects.all():
        boards.append(board.board)

    # Return the value you want as a dictionnary. You may add multiple values in here.
    return {'VERSION': version, 'UPDATE': update, 'BOARDS': boards}
