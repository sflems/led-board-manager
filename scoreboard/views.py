from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


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
        
        #TO DO: Expand on form validation
        try:
            # The request data must be encoded and the decoded due to a BOM error. Without this the form submissions are saved as slash escaped strings... but why? (Needs expert opinon.)
            new_config = request.POST['json'].encode().decode('utf-8-sig')
            new_settings = Settings.objects.create(config=json.loads(new_config))
            new_settings.save()
            
            # From django docs:
            # Return an HttpResponseRedirect to prevent data from being posted twice if a user hits the Back button.
            messages.success(request, "Your data has been saved!")
            return HttpResponseRedirect(reverse('index'))
        
        except:
            return render(request, "scoreboard/settings.html", { "error": "Form submission error.", "form":SettingsForm() })
            

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
