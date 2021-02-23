from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, JsonResponse
from django.core.exceptions import FieldError
from constance import config

from .forms import SettingsDetailForm
from django_jsonforms.forms import JSONSchemaForm
from .models import *
from . import services
import json, os, subprocess

notes = [
                    " (Not Active)",
                    " (Active)" 
                ]

# Create your views here.
@login_required
def index(request):

    games = services.todays_games()
    return render(request, "scoreboard/index.html", {"games":games,})

@login_required
def command(request):
    data = json.loads(request.body)
    if request.method == "PUT" and data.get("autostart"):
        try:
            # Autostart toggle option for autostart.sh or supervisor here
            pass
        
        except subprocess.CalledProcessError:
            return JsonResponse({
                "autostart": False,
            }, status=400)  
        else:
            pass 

    # Command to stop the web server
    if request.method == "PUT" and data.get("stopserver"):       
        try:
            # Checks if process is supervisor run
            if not services.gui_status()
                command = ["kill " + str(os.getpid())]
            else:
                command = ["sudo supervisorctl stop " + config.SUPERVISOR_GUI_NAME]
            
            subprocess.check_call(command, shell=True)
        
        except subprocess.CalledProcessError:
            return JsonResponse({
                "stopserver": False,
            }, status=400)  

        except ValueError:
            return JsonResponse({
                "stopserver": False,
            }, status=400)      
             

    if request.method == "PUT" and data.get("reboot"):
        try:
            #call = subprocess.call(["sudo", "reboot"])
            command = ["sleep 5 ; sudo reboot"]
            subprocess.check_call(command, shell=True)
            
        except subprocess.CalledProcessError:
            return JsonResponse({
                "reboot": False,
            }, status=400)
        else:
            return JsonResponse({
                "reboot": True
            }, status=202)    

    if request.method == "PUT" and data.get("shutdown"):
        try:
            command = "sleep 5 ; sudo shutdown -h now"
            subprocess.check_call(command, shell=True)
            
        except subprocess.CalledProcessError:
            return JsonResponse({
                "shutdown": False
            }, status=400)
        else:
            return JsonResponse({
                "shutdown": True
            }, status=202)
                    
class SettingsList(ListView):
    model = Settings

@login_required
def active_profile(request):
    if request.method == "GET":
        profile = Settings.objects.get(isActive=1)
        scoreboard_status = services.proc_status()

        return JsonResponse({
            "profile": profile.serialize(),
            "scoreboard_status": scoreboard_status
        }, status=200)

@login_required
def resource_monitor(request):
    if request.method == "GET":
        cpu = services.cpu()
        cputemp = services.cputemp()
        disk = services.disk()
        memory = services.memory()

        return JsonResponse({
            "cpu": cpu,
            "cputemp": cputemp,
            "disk": disk,
            "memory": memory
        }, status=200)

@login_required
def profiles(request, id):
    if request.method == "GET":
        profile = get_object_or_404(Settings, pk=id)
        if profile.id != 1 or profile.name.lower() != "default":
            # Settings Forms are instantiated with form_options and schema functions from services.py
            schema = services.schema()
            startval = profile.config
            options = services.form_options(startval)

            return render(request, "scoreboard/settings_edit.html", { 
                "detailform": SettingsDetailForm(instance=profile), 
                "JSONform": JSONSchemaForm(schema=schema, options=options, ajax=True),
                "profile_id": profile.pk,
                "profile_name": profile.name
                })
        else:
            messages.error(request, "Cannot edit the default profile!")
            return HttpResponseRedirect(reverse('profiles_list'))
        

    elif request.method == "PUT":
        try:
            profile = Settings.objects.get(pk=id)
            data = json.loads(request.body)

            if data.get("activated"):
                if not profile.isActive:
                    profile.isActive = True
                    profile.save()
                    messages.success(request, "\"" + profile.name + "\" activated.")
                    return JsonResponse({
                        "activated": True
                    }, status=202)
                else:
                    return JsonResponse({
                        "activated": false,
                        "profile":profile.name
                    }, status=400)

            if data.get("backup"):
                try:
                    path = profile.save_to_file().strip()
                    message = "Profile saved to " + path
                    return JsonResponse({
                        "backup": True,
                        "path": path
                    }, status=202)
                except:
                    return JsonResponse({
                        "backup": False,
                        "path": path
                    }, status=400)

            if data.get("delete"):
                try:
                    name = profile.name
                    profile.delete()
                    message = "\"" + name + "\" deleted successfully."
                    messages.success(request, message)
                    return JsonResponse({
                        "delete": True,
                    }, status=202)
                except:
                    return JsonResponse({
                        "delete": False,
                        "profile": profile.name,
                    }, status=400)

        except ObjectDoesNotExist:
            return render(request, "scoreboard/settings_create.html", {
                "error": "No profile found."
            })


    elif request.method == "POST":
        profile = get_object_or_404(Settings, pk=id)
        detailform = SettingsDetailForm(request.POST, instance=profile)
        new_config = json.loads(request.POST['json'].encode().decode('utf-8-sig'))

        if detailform.is_valid():
            profile.config = new_config
            profile.save(update_fields=['config'])
            detailform.save()
            message = "Your profile has been updated." + notes[profile.isActive]
            messages.success(request, message)

            return HttpResponseRedirect(reverse("profiles_list"), {"message": message,})

@login_required
def profiles_create(request):
    if request.method == "GET":
        schema = services.schema()
        startval = services.conf_default()
        options = services.form_options(startval)

        # Settings Forms are instantiated in forms.py
        detailform = SettingsDetailForm()
        return render(request, "scoreboard/settings_create.html", {
            "JSONform":JSONSchemaForm(schema=schema, options=options, ajax=True), 
            "detailform":detailform,
        })
        
    if request.method == "POST":
        detailform = SettingsDetailForm(request.POST)
        # The request data for the config json must be encoded and then decoded again as below due to a BOM error. Without this the form submissions are saved as slash escaped strings... but why? Possibly due to jsonforms encoding methods.
        new_config = json.loads(request.POST['json'].encode().decode('utf-8-sig'))

        if detailform.is_valid():           
            
            name = detailform.cleaned_data['name']
            isActive = detailform.cleaned_data['isActive']
            
            

            new_settings = Settings.objects.create(name=name, isActive=isActive, config=new_config)
            new_settings.save()

            message = "Your profile has been saved." + notes[isActive]
            messages.success(request, message)

            return HttpResponseRedirect(reverse("profiles_list"), {"message": message,})

        elif FieldError:
            schema = services.schema()
            startval = json.loads(request.POST['json'])
            options = services.form_options(startval)

            # JSONResponse to refill form? This isnt working.
            return render(request, "scoreboard/settings_create.html", { 
                "error": "Profile with this name exists.", 
                "detailform": SettingsDetailForm(request.POST), 
                "JSONform": JSONSchemaForm(schema=schema, options=options, ajax=True)
                })
        else:      
            return render(request, "scoreboard/settings_create.html", { 
                "error": "Invalid data. Please check your submission.", 
                "detailform": SettingsDetailForm(request.POST), 
                "JSONform": JSONSchemaForm(schema=schema, options=options, ajax=True)
                })
            

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
    
