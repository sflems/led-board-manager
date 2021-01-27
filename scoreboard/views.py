from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .forms import *
from .models import *
from .services import *
import json

# Create your views here.
def index(request):
    games = todays_games()
    return render(request, "scoreboard/index.html", {"games":games,})

@login_required
def settings_view(request):
    if request.method == "GET":
        # Settings Form is instantiated in forms.py
        form = SettingsForm()
        return render(request, "scoreboard/settings.html", {"form":form,})
        
    if request.method == "POST":
        new_config = request.POST
        new_settings = Settings.objects.create(config=new_config['json'])
        ## TODO: STOP CONFIG FROM SAVING AS AN \ ESCAPED STRING!
        new_settings.save()
        return render(request, "scoreboard/index.html", { "error": new_settings.config, })
            

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "scoreboard/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "scoreboard/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "scoreboard/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "scoreboard/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "scoreboard/register.html")
