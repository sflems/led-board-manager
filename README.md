# NHL LED Scoreboard Web GUI & Configurator
#### A Django based web app to configure an <a href="https://github.com/riffnshred/nhl-led-scoreboard">NHL LED Scoreboard</a> running on a Raspberry Pi.

## Table of Contents
  - [Description](#description)
  - [Features](#features)
  - [Disclaimer](#disclaimer)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Optional Steps](#optional-but-highly-suggested)
    - [Manual Installation](#manual-installation)
    - [Autostarting the Webserver](#auto-starting-the-server--boot)
    - [Updates](#updates)
    - [Removal / Uninstall](#removal--uninstall)
  - [Usage](#usage)
    - [Starting the Server](#to-start-the-webserver)
    - [Accessing the Server](#to-access-the-server)
    - [To Stop the Server](#to-stop-the-server)
    - [Default Login](#default-admin-login)
    - [Info & Troubleshooting](#info--troubleshooting)
  - [Screenshots](#screenshots)

_____________

## Description
Designed as a solution to manage the NHL LED Scoreboard project by [Joel Joannisse](https://github.com/riffnshred). 

The app uses a Django webserver to manage profiles in a simple SQLite database. Users can access the web interface which can be hosted on their local machine or network. The current `config.schema.json` found in the `nhl-led-scoreboard/config` directory generates an easy to use form to create a `config.json` file. At the moment, configurations you edit are validated against this current schema exclusively. It saves a new `config.json` in the `nhl-led-scoreboard/config` directory. The app also has the ability to backup configurations to file from the dashboard. 

JSON can also be edited manually in the `/admin` interface. __Be Careful!__ The entries in the admin panel are currently __not__ validated against the config schema. This allows you to enter custom configurations during testing.

_____________

## Features
- Today's NHL Games Dashboard
- Profiles Dashboard
  - Manage Configurations in an easy to use Dashboard
  - Create Configurations with a Simple Form (based on the current NHL LED Scoreboard schema)
  - Configuration/Profile Backup
- Supervisor Integration ([Optional](#option-1-create-a-supervisor-config-to-start-the-gui-with-gunicorn-preferred))
  - Activating A Profile Restarts the Scoreboard Process
  - Scoreboard Status Monitor
- Pi Commands
  - Stop Server
  - Reboot
  - Shutdown
- Profile Status & Resource Monitor
- Admin Dashboard
  - Profiles Management
  - User Management
  - WebGUI Defaults for Supervisor Program Names and Config Location (Admin Constance Tab or change `CONSTANCE_CONFIG` in `Capstone/settings.py`)

_____________

### Disclaimer
_(Work in Progress)_

This project is still in development. Development of the NHL LED Scoreboard is similarly evolving. They both rely on the external NHL API which, at any time may be inaccessible or updated. This app __does__ modify your configuration files in the `nhl-led-scoreboard/config` directory. While these files are cloned during installation, please backup any _prized_ configurations on your own accord.

_____________

## Requirements 
- [Raspberry Pi (Zero WH, 3B+, 3A+, 4B)](https://github.com/riffnshred/nhl-led-scoreboard)

- [NHL LED Scoreboard](https://github.com/riffnshred/nhl-led-scoreboard)

- [Hockey](https//www.nhl.com)

- [App Dependancies](requirements.txt)

## Installation
__Be sure to back up any previous configurations before use!!!__ The original files are overwritten and saved as `config.json.webgui.bak` and `config.schema.json.webgui.bak` in the `nhl-led-scoreboard/config/bak` subdirectory.

#### From the `/home/user` directory:
###### (or the same location as your `nhl-led-scoreboard` directory)

```
git clone --recursive https://github.com/sflems/nhl-led-scoreboard-webgui.git
cd nhl-led-scoreboard-webgui
```

#### Optional, but _Highly_ Suggested: 
_To run the server in a development environment, or if you have issues with dependencies, `virtualenv` can be a solution to create a separate "environment" for the server to run in._
```
sudo apt-get install python3-venv
python3 -m venv env
source env/bin/activate
```

_To exit the `virtualenv` at any time after installing, enter the command `deactivate` in the terminal._

_____________

#### Install (Cont.)
```
./install.sh
gunicorn Capstone.wsgi -b 0:9002
```
If all is working, you should then be able to access the app @ `YOUR_IP:9002` in the browser.

#### Default Login (Change me in the admin panel!)
Username: `admin`
Password: `scoreboard`

If you can't access the server and are using a firewall such as `ufw` or `iptables`, be sure to allow access _to your local network only_ over the `9002` port (or whatever you set it to if so). If you have ports 80/443 open on your Pi/Router, this site WILL be accessable by all, so be sure to have your firewall(s) in order. 

__To automatically start the webserver on reboot, be sure to follow the [Autostarting the Webserver](#auto-starting-the-server--boot) step.__

__See also: [Usage Instructions](#usage)__

## Manual Installation:
```
touch .secret.txt
chmod g+w .secret.txt
```

###### Back up originals and then copy the updated Schema to the config folder in the nhl-led-scoreboard directory.
```
mkdir -p ../nhl-led-scoreboard/config/bak/original 
mv ../nhl-led-scoreboard/config/config.schema.json ../nhl-led-scoreboard/config/bak/original/$(date +"%Y_%m_%d_%I_%M_%p")-config.schema.json
cp ../nhl-led-scoreboard/config/config.json ../nhl-led-scoreboard/config/bak/original/$(date +"%Y_%m_%d_%I_%M_%p")-config.json
```

###### THIS NEEDS TO BE UPDATED FOR THE 2021-2022 Season!!! Updated schema file with divisions is in /nhl-led-scoreboard-webgui/scoreboard/static/schema dir.
```
cp ./scoreboard/static/schema/config.schema.json ../nhl-led-scoreboard/config/config.schema.json
```

###### Install the app requirements and dependencies from the included requirements.txt file:
`pip3 install -r requirements.txt`

###### Once complete, we'll make, migrate and fill our sqlite3 database with the supplied teams data in the fixtures folder:

First, run:

`python3 manage.py makemigrations`

Followed by:

`python3 manage.py migrate`

And lastly:

`python3 manage.py loaddata teams.json`

Either follow the next step to setup server autostart, or see [usage instructions](#usage) for more details.

## Auto-Starting the server @ boot: 
#### OPTION 1: Create a Supervisor Config to start the GUI with Gunicorn (PREFERRED):
Create a new supervisor config with the command:
`sudo nano /etc/supervisor/conf.d/scoreboard-webgui.conf`

And copy into it the following contents:
_Be sure to change the `pi` username _if_ you have done so._
```
[program:scoreboard-gui]
command=/home/pi/.local/bin/gunicorn Capstone.wsgi -b 0:9002
directory=/home/pi/nhl-led-scoreboard-webgui
autostart=true
user=pi
```

###### _If_ you setup a `virtualenv`, change the `autorun.sh` contents to the following:
```
[program:scoreboard-webgui]
command=/home/pi/nhl-led-scoreboard-webgui/env/bin/gunicorn Capstone.wsgi -b 0:9002
directory=/home/pi/nhl-led-scoreboard-webgui
autostart=true
user=pi
```

#### OPTION 2: Create a script and use `rc.local` to autostart the devserver on startup:
We're going to use the Raspberry Pi's `/etc/rc.local` file to start our script on boot. In the `/nhl-led-scoreboard-webgui` folder, create a new file using:

Enter `sudo nano /etc/rc.local` to add the following line before `exit 0`:

```
su user -c '/home/user/nhl-led-scoreboard-webgui/autorun.sh >> /tmp/scoreboard-gui.log 2>&1'
```
...substituting your own username for `user`, or `pi` if it is still the default. This will also create a log file for the server: `/tmp/scoreboard-gui.log`. You can tail the log with the following command:

`tail -f -n 100 /tmp/scoreboard-gui.log`

###### _If_ you setup a `virtualenv`, change the `autorun.sh` contents to the following:
```
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${DIR}
${DIR}/env/bin/gunicorn Capstone.wsgi -b 0:9002

exit 0
```

Alternatively, you can setup a [crontab](https://www.raspberrypi.org/documentation/linux/usage/cron.md), [systemd](https://www.raspberrypi.org/documentation/linux/usage/systemd.md), or another method of your choice to autostart the app.

## Updates
The latest update notes can be found under the [project releases](https://github.com/sflems/nhl-led-scoreboard-webgui/releases). 

__If you are using `virtualenv`, be sure to [activate]((#optional-but-highly-suggested)) it before updating.__

When updating, or if stated in the release notes, it may be necessary to run the update script:
```./update.sh``` 
Then, restart the web server.

Alternatively, manually enter the following commands:
```
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py load data teams.json
```
Then, restart the web server.

## Removal / Uninstall
##### To remove the webserver:
```
cd
sudo rm -rfv nhl-led-scoreboard-webgui
```
The `nhl-led-scoreboard/config/bak` directory created at install will remain. It contains any profiles backed up from the GUI as well the original schema and config files.

##### Remove the Supervisor Configuration if present:
```
sudo rm /etc/supervisor/conf.d/scoreboard-webgui.conf
```

##### Remove the `rc.local` Configuration if present:
```
sudo nano /etc/rc.local
```
...and remove the server's autorun.sh script line.

## Usage
__Be sure to back up any previous configurations before use!!!__
### To start the webserver:

To start the server, enter `gunicorn Capstone.wsgi -b 0:9002` in your console from the directory that you installed the app in.
You can also run `./autorun.sh` from the same location.

This command, and the default configuration, start the server on `0.0.0.0` and port `9002` making it available to any connected devices on your local network. Alternatively, you can run the server on a different port, e.g. `0:8000`, `0:PORT`, or available to _just_ the `localhost` machine by running `gunicorn Capstone.wsgi -b 127.0.0.1:9002`.

__Note__: *This server should not be served over a public connection or used in a production environment. If you wish to view the scoreboard WebGUI remotely, you can do so securely by accessing your local network using a VPN service.*

_____________

### To access the server:
Access the dashboard at `YOUR_IP:PORT` in the browser.

###### Default Login (Change me in the admin panel!)

Username: `admin`

Password: `scoreboard`

_____________

### To stop the server:
In a terminal shell with the server running, `Ctrl` + `C` will terminate the process.

###### If the server is running in the background:
`pkill -f Capstone.wsgi`

...Or to find the process IDs, enter `ps aux | grep gunicorn`

Example response:
```
    user@raspi:~ $ ps aux | grep gunicorn
--> user      6300 26.6  0.8  38236 33364 pts/0    S+   00:22   0:01 gunicorn Capstone.wsgi -b 0:9002
    user      6319  0.0  0.0   3160  1536 pts/1    S+   00:22   0:00 grep --color=auto gunicorn
    user@raspi:~ $ 
```
This is the second number in the table following the username (Use caution if you have more than one python/Django server running!). Change the `PID` in the following command to that number to kill the server:

`kill -9 PID`

Better yet... simply stop the server from supervisor, or the dashboard  :).

_____________

### Default Admin Login

`YOUR_IP:9002/admin`

Username: `admin`

Password: `scoreboard`

__Please change this password!__ You can do this by visiting `YOUR IP:PORT/admin` and clicking the change password button. Email currently isn't configured.

_____________

## Info / Troubleshooting
- After updating, it may be necessary to update the database. See [Updates](#updates) for more info.

- When a config is activated, the config.json contents are replaced with an updated configuration. You can do this on the profiles page. Your previous config.json is still "active" until you active one here.

- When a profile is backed up, a file is created in the same folder as profile.config.json.bak. It's path is displayed as a message in the browser. Deleted profiles do not delete the config.json or .bak files; it only removes them from the Django Sqlite database. 

- The GUI Defaults (ie Scoreboard path, Supervisor Program Name, etc.) can be changed in the Constance admin panel. Alternatively, they can be modified manually in the `Capstone/settings.py` file under the `CONSTANCE_CONFIG` variable.
- File Structure
  ```
  nhl-led-scoreboard-webgui/      <-- Project Base Folder
  |
  ├── assets/                     <-- Assets used in README.md.
  |
  ├── Capstone/                   <-- Capstone Django Project Directory
  │   ├── __init__.py
  │   ├── asgi.py
  │   ├── settings.py             <-- Django server config / settings.
  │   ├── urls.py                 <-- Django server base URLs.
  │   └── wsgi.py                 <-- Used to launch nhl-led-scoreboard-webgui.
  |
  ├── env/                        <-- Virtual environent folder (if installed).
  |
  ├── scoreboard/                 <-- Scoreboard Django App Directory
  |   |
  │   ├── fixtures/               <-- Contains teams.json DB initialization data as well as sample config JSON files for the nhl-led-scoreboard.
  │       ├── config.json
  │       ├── config.schema.json
  │       └── teams.json
  │   ├── migrations/           
  │   ├── static/
  │       ├── fonts/              <-- Fonts used.
  │       ├── schema/             <-- Schema Files used during install for correct django-jsonforms function.
  │       └── scoreboard/         <-- CSS / SVG's / JS for Pages, JSONEditor, and JSCookie.
  |   ├── templates/
  │       └── scoreboard/         <-- Django HTML Templates for Various Pages
  │   ├── __init__.py
  │   ├── asgi.py
  │   ├── admin.py
  │   ├── apps.py
  │   ├── forms.py                <-- Forms: SettingsDetailForm setup, used for name and active state of config profiles. The JSON forms are insantiated from services.py.
  │   ├── LICENSE
  │   ├── models.py               <-- Models: Settings, Constance, User/Profile, Teams
  │   ├── services.py             <-- Services: Various functions used throughout the scoreboard app, ie JSONForms, NHL API, Resource Monitor Functions, etc.
  │   ├── tests.py
  │   ├── urls.py                 <-- Scoreboard specific URLs setup.
  │   └── views.py                <-- Views created for scoreboard app.
  |
  ├── .secret.txt                   <-- Created by secret-key-generator for key randomization.
  ├── autorun.sh                    <-- Server start script.
  ├── db.sqlite3                    <-- Nhl-led-scoreboard-webgui database.
  ├── install.sh                    <-- App install script. Automates django installation / installs requirements, and sets up database.
  ├── LICENSE
  ├── manage.py                     <-- Django manage.py file used to operate project.
  ├── README.md                     <-- Just RTFM.
  ├── requirements.txt              <-- Project requirements, used by pip and install.sh.
  ├── TODO.txt                      <-- To-do list.
  ├── update.sh                     <-- Script used to simplify if required in an update. Runs migration/loaddata commands, etc.
  └── webgui-log.out                <-- Log created by install.sh script. 
  ```
_____________

## Screenshots / Demo
##### It's Mobile Freindly Too! (Responsive)
I encourage anyone interested to take a quick peek at the demo on YouTube:

[![Web GUI YouTube Demo Video](https://img.youtube.com/vi/5byJf5v6Hnc/0.jpg)](https://www.youtube.com/watch?v=5byJf5v6Hnc)

###### Dashboard
  <img src="/assets/images/LED Scoreboard Configurator - Dashboard.png" alt="LED Scoreboard Configurator - Dashboard" width="100%"/>
  
###### Profiles Dashboard
  <img src="/assets/images/LED Scoreboard Configurator - Profiles Dashboard.png" alt="LED Scoreboard Configurator - Profiles Dashboard" width="100%"/>
  
###### Create/Edit A Profile
  <img src="/assets/images/LED Scoreboard Configurator - Create_Edit A Profile.png" alt="LED Scoreboard Configurator - Create_Edit A Profile" width="100%"/>
  
###### Settings Admin
  <img src="/assets/images/LED Scoreboard Configurator - Settings Admin.png" alt="LED Scoreboard Configurator - Settings Admin" width="100%"/>

### Please let me know if you experience any bugs, feature suggestions or issues. Enjoy!
