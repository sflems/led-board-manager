from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import FieldError, ValidationError
from constance import config
from time import sleep

from .forms import SettingsDetailForm
from django_jsonforms.forms import JSONSchemaForm
from .models import Settings, BoardType
from . import services
import json, os, subprocess

# For Profile Activation Messages
notes = [
    " (Not Active)",
    " (Active)"
]

# Create your views here.
@login_required
def index(request):

    games = services.todays_games()
    return render(request, "scoreboard/index.html", {"games": games, })

@login_required
def command(request):
    data = json.loads(request.body)

    # Command to start/stop the active scoreboard
    profile = Settings.objects.get(isActive=1)
    if request.method == "PUT" and data.get("sb_command"):
        try:
            if data.get("sb_command") == "sb_start":
                command = ["sudo supervisorctl restart boards:" + profile.boardType.supervisorName]
            else:
                command = ["sudo supervisorctl stop boards:" + profile.boardType.supervisorName]
            
            subprocess.check_call(command, shell=True)
            sleep(3)
            status = profile.boardType.proc_status()

            if data.get("sb_command") == "sb_start" and status:
                return JsonResponse({
                    "sb_success": True,
                    "sb_status": status,
                }, status=202)
            elif data.get("sb_command") == "sb_start" and not status:
                return JsonResponse({
                    "sb_success": False,
                    "sb_status": status,
                    "error": "Unable to start scoreboard process."
                }, status=400)

            if data.get("sb_command") == "sb_stop" and not status:
                return JsonResponse({
                    "sb_success": True,
                    "sb_status": status,
                }, status=202)
            elif data.get("sb_command") == "sb_stop" and status:
                return JsonResponse({
                    "sb_success": False,
                    "sb_status": status,
                    "error": "Unable to stop scoreboard process, or no running process found."
                }, status=400)
        
        except subprocess.CalledProcessError as error:
            return JsonResponse({
                "sb_success": False,
                "error": str(error),
            }, status=400)

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
            if not services.gui_status():
                command = ["sleep 5 ; kill " + str(os.getpid())]
            else:
                command = ["sleep 5 ; sudo supervisorctl stop " + config.SUPERVISOR_GUI_NAME]
            
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
            command = ["sleep 5 ; sudo reboot"]
            subprocess.check_call(command, shell=True)
            return JsonResponse({
                "reboot": True
            }, status=202)

        except subprocess.CalledProcessError:
            return JsonResponse({
                "reboot": False,
            }, status=400)
            

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

# TODO: Add a check to see if profile matches actual config.json found in scoreboard/config directory.
@login_required
def active_profile(request):
    if request.method == "GET":
        try:
            profile = Settings.objects.get(isActive=1)
            return JsonResponse({
                "profile": profile.serialize(),
                "scoreboard_status": profile.boardType.proc_status()
            }, status=200)

        except Exception as e:
            return JsonResponse({
                "error": str(e)
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
            return render(request, "scoreboard/settings_edit.html", {
                "detailform": SettingsDetailForm(instance=profile),
                "JSONform": JSONSchemaForm(schema=profile.boardType.schema(), options=services.form_options(profile.config), ajax=True),
                "profile_id": profile.pk,
                "profile_name": profile.name
            })
        else:
            messages.error(request, "Cannot edit the default profile!")
            return HttpResponseRedirect(reverse('profiles_list'))

    elif request.method == "PUT":
        profile = get_object_or_404(Settings, pk=id)
        data = json.loads(request.body)

        if data.get("activated"):
            try:
                if not profile.isActive:
                    profile.isActive = True
                    profile.save()
                    messages.success(request, "\"" + profile.name + "\" activated.")
                    return JsonResponse({
                        "activated": True
                    }, status=202)
            except ValueError as error:
                return JsonResponse({
                    "activated": False,
                    "profile": profile.name,
                    "error": str(error)
                }, status=404)

        if data.get("backup"):
            try:
                path = profile.save_to_file().strip()
                return JsonResponse({
                    "backup": True,
                    "path": path
                }, status=202)
            except ValueError as error:
                return JsonResponse({
                    "backup": False,
                    "error": str(error)
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
            except Exception:
                return JsonResponse({
                    "delete": False,
                    "profile": profile.name,
                }, status=400)

    elif request.method == "POST":
        try:
            profile = get_object_or_404(Settings, pk=id)
            detailform = SettingsDetailForm(request.POST, instance=profile)
            new_config = json.loads(request.POST['json'].encode().decode('utf-8-sig'))
            print(profile, detailform, new_config)

            if detailform.is_valid():
                profile.config = new_config
                profile.save(update_fields=['config'])
                message = "Your profile has been updated." + notes[profile.isActive]
                messages.success(request, message)
                return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })

        except Exception as e:
            message = "Warning. ({})".format(e)
            messages.info(request, message)
            return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })
        except ValidationError as e:
            message = "Warning. ({})".format(e)
            messages.info(request, message)
            return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })
        except ValueError as e:
            message = "Warning. ({})".format(e)
            messages.info(request, message)
            return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })
        except FieldError as e:
            message = "Warning. ({})".format(e)
            messages.info(request, message)
            return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })

@login_required
def profiles_create(request, board):
    board_type = get_object_or_404(BoardType, pk=board)
    if request.method == "GET":
        return render(request, "scoreboard/settings_create.html", {
            "detailform": SettingsDetailForm(initial={'name':"", 'boardType': board_type}),
            "JSONform": JSONSchemaForm(schema=board_type.schema(), options=services.form_options({}), ajax=True),
            "boardtype": board,
        })

    if request.method == "POST":
        detailform = SettingsDetailForm(request.POST)
        detailform.is_valid()
        try:
            # The request data for the config json must be encoded and then decoded again as below due to a BOM error.
            # Without this the form submissions are saved as slash escaped strings... but why? Possibly due to jsonforms encoding methods.
            new_config = json.loads(request.POST['json'].encode().decode('utf-8-sig'))
            name = detailform.cleaned_data['name']
            isActive = detailform.cleaned_data['isActive']
            new_settings = Settings.objects.create(name=name, isActive=isActive, config=new_config, boardType=board_type)
            new_settings.save()

            message = "Your profile has been saved." + notes[isActive]
            messages.success(request, message)

            return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })

        except Exception as e:
            message = "Warning. ({})".format(e)
            messages.info(request, message)
            return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })
        except ValidationError as e:
            message = "Warning. ({})".format(e)
            messages.info(request, message)
            return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })
        except ValueError as e:
            message = "Warning. ({})".format(e)
            messages.info(request, message)
            return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })
        except FieldError as e:
            message = "Warning. ({})".format(e)
            messages.info(request, message)
            return HttpResponseRedirect(reverse("profiles_list"), {"message": message, })
        

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
