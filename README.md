# LED Board Manager
#### A Django based web app to configure an <a href="https://github.com/riffnshred/nhl-led-scoreboard">NHL LED Scoreboard</a>, and others, running on a Raspberry Pi.
 
#### Latest Releases
##### LED Board Manager
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/sflems/led-board-manager?label=version)](https://github.com/sflems/led-board-manager/releases) [![Django Tests](https://github.com/sflems/led-board-manager/actions/workflows/python-app.yml/badge.svg)](https://github.com/sflems/led-board-manager/actions/workflows/python-app.yml)

##### NHL LED Scoreboard:
[![GitHub release (latest by date)](https://badgen.net/github/release/riffnshred/nhl-led-scoreboard?label=Version)](https://github.com/riffnshred/nhl-led-scoreboard/releases/latest) [![Create Release - Image](https://github.com/falkyre/nhl-led-scoreboard-img/actions/workflows/main.yml/badge.svg)](https://github.com/falkyre/nhl-led-scoreboard-img/actions/workflows/main.yml)

## Table of Contents
  - [Description](#description)
  - [Features](#features)
    - Config Generator
    - Boards/Profile Manager (NEW!)
  - [Disclaimer](#disclaimer)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [First Steps](#first-steps)
    - [Manual Installation](#manual-installation)
    - [Autostarting the Webserver](#auto-starting-the-server--boot)
    - [Updates](#updates)
    - [Removal / Uninstall](#removal--uninstall)
  - [Usage](#usage)
    - [Starting the Server](#to-start-the-webserver)
    - [Accessing the Server](#to-access-the-server)
    - [To Stop the Server](#to-stop-the-server)
    - [Default Login](#default-admin-login)
    - [Info](#info)
    - [Troubleshooting](#troubleshooting)
  - [Screenshots](#screenshots--demo)

_____________

## Description
Designed as a solution to manage the NHL LED Scoreboard project by [Joel Joannisse](https://github.com/riffnshred), as well as custom board integration. 

The app uses a Django webserver to manage profiles in a simple SQLite database. Users can access the web interface which can be hosted on their local machine or network. The current `config.schema.json` found in the `nhl-led-scoreboard/config` directory generates an easy to use form to create a `config.json` file. It saves a new `config.json` in the `nhl-led-scoreboard/config` directory and restarts your board process to implement any changes on the fly! 

JSON can also be edited manually in the `/admin` interface. The admin app also has the ability to backup configurations to file from the dashboard and set various scoreboard flags on the fly.

Boards and their paths/settings may also be added or configured in the admin panel.
_____________

## Features
- GUI / Today's NHL Games Dashboard
  - Swap between various board projects ie. NHL, NFL, MLB, etc.
  - Easily Toggle your scoreboard On and Off
  - Profile Status & Resource Monitor
- Profiles Dashboard
  - Manage Configurations on the Fly
  - Create Configurations with a Simple Form (schema dependant)
  - Configuration/Profile Backup
- Supervisor Integration
  - Activating A Profile Updates the Board in Real Time
  - Scoreboard Status Monitor
- Pi Commands
  - Scoreboard On/Off Toggle
  - Stop Server
  - Reboot
  - Shutdown
- Admin Dashboard
  - Boards Management (NHL / NFL / MLB / etc.)
  - Profiles Management
  - User Management
  - Scoreboard Flags (ie. `--led-brightness`, `--led-gpio-mapping`, `--update-check`, etc.)
  - WebGUI Defaults (ie. Default paths, Supervisor `[program:names]`)
- REST API (W.I.P.)
  - Interact with the board management backend API routes. (via http://`YOUR_IP`:9002/api)

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

#### Compatible Boards:
- [NFL LED Scoreboard](https://github.com/mikemountain/nfl-led-scoreboard)

- [MLB LED Scoreboard](https://github.com/MLB-LED-Scoreboard/mlb-led-scoreboard)

- [Stonks](https://github.com/rdefeo/stonks)

- ...and similar forks.

## Installation
__Be sure to back up any previous configurations before use!!!__

#### From the `/home/pi` directory:
###### (or the same location as your `nhl-led-scoreboard` directory)

```
git clone --recursive https://github.com/sflems/led-board-manager.git
cd led-board-manager
```
#### First Steps

##### Install `supervisor` (as root): 
###### You can skip to [Auto-Starting the Server](#auto-starting-the-server--boot) if you have an active `supervisor' installation. Then return here for the _easy_ install method.
```
su
mkdir /etc/supervisor && cp /home/pi/led-board-manager/scoreboard/static/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
chmod 644 /etc/supervisor/supervisord.conf

mkdir /etc/supervisor/conf.d && cp /home/pi/led-board-manager/scoreboard/static/supervisor/scoreboard.conf /etc/supervisor/conf.d/scoreboard.conf
chmod 644 /etc/supervisor/conf.d/scoreboard.conf

cp /home/pi/led-board-manager/scoreboard/static/supervisor/supervisord.service /etc/systemd/system/supervisord.service
chmod 644

python3 -m pip install supervisor

systemctl unmask supervisord
systemctl enable supervisord 
su pi

mv sample.supervisor-daemon.conf supervisor-daemon.conf
```

###### Sample configurations can be found in the [`nhl-led-scoreboard-img`](https://github.com/falkyre/nhl-led-scoreboard-img/tree/master/stage2/06-supervisor/files) project, by [@falkyre](https://github.com/falkyre).

###### Install and Start `python3-venv`: 
_To run the server in a development environment, `python3-venv` can be a solution to create a separate "environment" for the server to run in._
```
sudo apt install python3-venv
python3 -m venv env
./scripts/install.sh
sudo supervisorctl reread
```
Once finished, you can start the server with:
```
source env/bin/activate
gunicorn Capstone.wsgi -b 0:9002
```
If all is working, you should then be able to access the app @ `YOUR_IP:9002` in the browser. You can deactivate the enve with the command `deactivate`.

#### Default Login (Change me in the admin panel!)
Username: `admin`

Password: `scoreboard`

If you can't access the server and are using a firewall such as `ufw` or `iptables`, be sure to allow access _to your local network only_ over the `9002` port (or whatever you set it to if so). If you have ports 80/443 open on your Pi/Router, this site WILL be accessable by all, so be sure to have your firewall(s) in order. 

__See also: [Usage Instructions](#usage)__

_____________

## Manual Installation:
#### From the `/home/pi` directory:
###### (or the same location as your `nhl-led-scoreboard` directory)

```
git clone --recursive https://github.com/sflems/led-board-manager.git
cd led-board-manager
touch .secret.txt
chmod g+w .secret.txt
```

##### Install `supervisor` (as root): 
###### Skip to [Auto-Starting the Server](#auto-starting-the-server--boot) if you have an active `supervisor' installation.
```
su
mkdir /etc/supervisor && cp /home/pi/led-board-manager/scoreboard/static/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
chmod 644 /etc/supervisor/supervisord.conf

mkdir /etc/supervisor/conf.d && cp /home/pi/led-board-manager/scoreboard/static/supervisor/scoreboard.conf /etc/supervisor/conf.d/scoreboard.conf
chmod 644 /etc/supervisor/conf.d/scoreboard.conf

cp /home/pi/led-board-manager/scoreboard/static/supervisor/supervisord.service /etc/systemd/system/supervisord.service
chmod 644

python3 -m pip install supervisor

systemctl unmask supervisord
systemctl enable supervisord 
su pi

mv sample.supervisor-daemon.conf supervisor-daemon.conf
```

If you have the [MLB Board](https://github.com/MLB-LED-Scoreboard/mlb-led-scoreboard) installed (in default location):
```
cp ~/led-board-manager/scoreboard/static/schema/mlb.config.schema.json ~/mlb-led-scoreboard/config.schema.json
```
If you have the [NFL Board](https://github.com/mikemountain/nfl-led-scoreboard) installed (in default location):
```
cp ~/led-board-manager/scoreboard/static/schema/nfl.config.schema.json ~/nfl-led-scoreboard/config.schema.json
```
Follow either command with:
```
sudo supervisorctl reread
```

###### Sample configurations can be found in the [`nhl-led-scoreboard-img`](https://github.com/falkyre/nhl-led-scoreboard-img/tree/master/stage2/06-supervisor/files) project, by [@falkyre](https://github.com/falkyre).

##### Install `python3-venv` and create the Web Gui environment: 
```
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate
```

Your shell should have the `(env)` prepended if active:
```
(env) pi@raspberrypi:~/led-board-manager $ 
```

_To exit the `(env)` at any time __after__ installing and running the `test` step, enter the command `deactivate` in the terminal._

##### Install the app requirements and dependencies from the included requirements.txt file:
`pip3 install -r requirements.txt`

##### Once complete, we'll make, migrate and fill our sqlite3 database with the supplied teams data in the fixtures folder:

First, run:

 ```
 python3 manage.py makemigrations
 python3 manage.py migrate
 python3 manage.py loaddata teams.json
 python3 manage.py test
 ```

Either follow the next step to setup server autostart, or see [usage instructions](#usage) for more details.

## Auto-Starting the server @ boot: 
See the wiki for the complete [Auto-Start instructions](https://github.com/sflems/led-board-manager/wiki/Auto-Starting-the-server-@-Boot).

## Updates
The latest update notes can be found under the [project releases](https://github.com/sflems/led-board-manager/releases). 

[Stop the server](#to-stop-the-server), then:
```
cd led-board-manager/
git reset --hard
git checkout main
git pull
```

_When updating, or if stated in the release notes, it may be necessary to run the update script from the `led-board-manager` directory._
```
./scripts/update.sh
``` 
Then, restart the web server.

Alternatively, manually enter the following commands:
```
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata teams.json
python3 manage.py test
```
Then, restart the web server. You can `deactivate` the `(env)` if you are using the `./scripts/autorun.sh` script or `supervisor`.

## Removal / Uninstall
##### To remove the webserver:

`deactivate` the `(env)`, then:

```
cd
sudo rm -rfv led-board-manager
```
Any profiles backed up from the GUI and the `config.json` file will remain in the `config/` directories.

##### Remove the Supervisor Configuration if present. Change the following:
```
[include]
files = conf.d/*.conf /home/pi/led-board-manager/supervisor-daemon.conf
```
Back to:
```
[include]
files = conf.d/*.conf
```

##### Remove the `rc.local` Configuration if present:
```
sudo nano /etc/rc.local
```
...and remove the server's autorun.sh script line.

## Usage
__Be sure to back up any previous configurations before use!!!__
### To start the webserver:

To start the server manually, and from the `led-board-manager` directory, enter:
```
source env/bin/activate && gunicorn Capstone.wsgi -b 0:9002
```

### To start the webserver with a script:
Simply run `./scripts/autorun.sh` from the same location.

This command, and the default configuration, start the server on `0.0.0.0` and port `9002` making it available to any connected devices on your local network. Alternatively, you can run the server on a different port, e.g. `0:8000`, `0:PORT`, or available to _just_ the `localhost` machine by running:
```
source env/bin/activate
gunicorn Capstone.wsgi -b 127.0.0.1:9002
```

__Note__: *This server should not be served over a public connection or used in a production environment. If you wish to view the scoreboard WebGUI remotely, you can do so securely by accessing your local network using a VPN service.*

_____________

### To access the server:
Access the dashboard at `YOUR_IP:PORT` in the browser.

###### Default Login (Change me in the admin panel!)

Username: `admin`

Password: `scoreboard`

_____________

### To stop the server:
In a terminal shell with the server running, `Ctrl` + `C` will terminate the process. Then, `deactivate` at any time to stop the `venv`.

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

_Better yet_... simply stop the server from supervisor, or the dashboard  :).

_____________

### Default Admin Login

`YOUR_IP:9002/admin`

Username: `admin`

Password: `scoreboard`

__Please change this password!__ You can do this by visiting `YOUR IP:PORT/admin` and clicking the change password button. Email currently isn't configured.

_____________

## Info 
- The supervisor configuration is updated when saving flag settings or BoardType settings in the admin panel.
- When a profile is activated, the appropriate `config.json` contents are replaced with an updated configuration. You can do this on the profiles page. Your previous config.json is still "active" until you activate one here.
- When a profile is backed up, a file is created in the same folder as `profile_name.config.json`. It's path and name are displayed as a message in the browser. 
- Deleted profiles do not delete the `config.json` files; it only removes them from the Django Sqlite database. 
- The `supervisor-daemon.conf` used by the `led-board-manager` app prefixes any configured BoardTypes with `boards:`.
  - These programs are grouped in supervisor with the `boards:` prefix.
  - `sudo supervisorctl restart scoreboard` would become `sudo supervisorctl restart boards:scoreboard`.
- The GUI Defaults (ie Scoreboard path, Supervisor Program Name, etc.) can be changed in the admin panel. Alternatively, they can be modified manually in the `Capstone/settings.py` file under the `CONSTANCE_CONFIG` variable.
  - Scoreboard Flags (ie. `--led-brightness`, `--led-gpio-mapping`, `--update-check`, etc.) can be changed here too.

## Troubleshooting
- After updating, it may be necessary to update the database. See [Updates](#updates) for more info.
- `403 ERROR` when trying to access site: The Django CSRF method uses cookies to send a CSRF token with form submissions. Try adding your device IP to the allowed site cookies in your browser settings. If this doesn't work, please open an [issue](https://github.com/sflems/led-board-manager/issues).

_____________

## Screenshots / Demo
##### It's Mobile Friendly Too! (Responsive)
I encourage anyone interested to take a quick peek at the demo on YouTube:

[![Web GUI YouTube Demo Video](https://img.youtube.com/vi/5byJf5v6Hnc/0.jpg)](https://www.youtube.com/watch?v=5byJf5v6Hnc)

_____________

###### Dashboard
  <img src="/assets/images/LED Scoreboard Configurator - Dashboard.png" alt="LED Scoreboard Configurator - Dashboard" width="100%"/>
  
###### Profiles Dashboard
  <img src="/assets/images/LED Scoreboard Configurator - Profiles Dashboard.png" alt="LED Scoreboard Configurator - Profiles Dashboard" width="100%"/>
  
###### Create/Edit A Profile
  <img src="/assets/images/LED Scoreboard Configurator - Create_Edit A Profile.png" alt="LED Scoreboard Configurator - Create_Edit A Profile" width="100%"/>
  
###### Settings Admin
  <img src="/assets/images/LED Scoreboard Configurator - Settings Admin.png" alt="LED Scoreboard Configurator - Settings Admin" width="100%"/>

###### Boards Admin
  <img src="/assets/images/LED Scoreboard Configurator - Boards Admin.png" alt="LED Scoreboard Configurator - Boards Admin" width="100%"/>
### Please let me know if you experience any bugs, feature suggestions or issues. Enjoy!
