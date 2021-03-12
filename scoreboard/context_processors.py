from django.conf import settings
from .services import gui_update_check

# This is a context processor to add custom {{ variables }} to templates.
def version(request):
    update = gui_update_check()
    version = settings.VERSION
    # Return the value you want as a dictionnary. You may add multiple values in here.
    return {'VERSION': version, 'UPDATE': update}
    