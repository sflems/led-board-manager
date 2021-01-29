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
        # Settings Forms are instantiated in forms.py
        detailform = SettingsDetailForm()
        JSONform = SettingsJSONForm()
        return render(request, "scoreboard/settings.html", {
            "JSONform":JSONform, 
            "detailform":detailform,
        })
        
    if request.method == "POST":
        detailform = SettingsDetailForm(request.POST)

        if detailform.is_valid():
        
            #TO DO: Expand on form validation
            try:
                ''' 
                    The request data for the config json must be encoded and the decoded again as below due to a BOM error. Without this the form submissions are saved as slash escaped strings... but why? Possibly due to jsonforms encoding methods.
                '''
                name = detailform.cleaned_data['name']
                isActive = detailform.cleaned_data['isActive']
                new_config = request.POST['json'].encode().decode('utf-8-sig')

                new_settings = Settings.objects.create(name=name, isActive=isActive, config=json.loads(new_config))
                

                '''
                    From django docs:
                    Return an HttpResponseRedirect to prevent data from being posted twice if a user hits the Back button.
                ''' 
                if new_settings.isActive.exists():
                    
                    if Settings.objects.filter(isActive=True):
                        active_profiles = Settings.objects.filter(isActive=True).exclude(name=new_settings.name)
                        for profile in active_profiles:
                            profile.isActive = False
                            profile.save()

                    '''
                    Insert filesystem saving logic (and scoreboard restart logic?) here.
                    '''
                    new_settings.save()
                    messages.success(request, "Your profile has been saved and set as the active profile.")
                    return HttpResponseRedirect(reverse('index'))
                   
                else:
                    new_settings.save()
                    messages.success(request, "Your profile has been saved.")
                    return HttpResponseRedirect(reverse('index'))
            
            except:
                return render(request, "scoreboard/settings.html", { "error": "Form submission error.", "jsonform":SettingsJSONForm(request.POST), "detailform":SettingsDetailForm(request.POST) })
                

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