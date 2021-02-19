# NHL LED Scoreboard Web GUI & Configurator
#### A Django based web app to configure an <a href="https://github.com/riffnshred/nhl-led-scoreboard">NHL LED Scoreboard</a> running on a Raspberry Pi.

## Description
Designed as a solution to manage the NHL LED Scoreboard project by [Joel Joannisse](https://github.com/riffnshred). 

The app uses a Django webserver to manage profiles in a simple SQLite database. Users can access the web interface which can be hosted on their local machine or network. The current `config.schema.json` found in the `nhl-led-scoreboard/config` directory generates an easy to use form to create a `config.json` file. At the moment, configurations you edit are validated against this current schema exclusively. It the saves a new `config.json` in the `nhl-led-scoreboard/config` directory. The app also has the ability to backup configurations to file from the dashboard. 

JSON can also be edited manually in the `/admin` interface. __Be Careful!__ The entries in the admin panel are currently __not__ validated against the config schema. This allows you to enter custom configurations during testing.

_____________

### Disclaimer
_(Work in Progress)_

This project is still in development. Development of the NHL LED Scoreboard is similarly evolving. They both rely on the external NHL API which, at any time may be inaccessible or updated. This app does modify your configuration files in the `nhl-led-scoreboard/config` directory. While these are backed up during installation, please backup any _prized_ configurations on your own accord.

_____________

## Table of Contents
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Optional Steps](#optional-but-suggested)
    - [Manual Installation](#manual-installation)
  - [Screenshots](#screenshots)
  - [Usage](#usage)
    - [Starting the Webserver](#to-start-the-webserver)
    - [Accessing the Server](#to-access-the-server)
    - [Autostarting the Webserver](#auto-starting-the-server--boot)
    - [To Stop the Server](#to-stop-the-server)
    - [Default Login](#default-admin-login)
    - [Info](#info)
_____________

## Requirements 
- [Raspberry Pi (Zero WH, 3B+, 3A+, 4B)](https://github.com/riffnshred/nhl-led-scoreboard)

- [NHL LED Scoreboard](https://github.com/riffnshred/nhl-led-scoreboard)

- [Hockey](https//www.nhl.com)

- [App Dependancies](requirements.txt)

_____________

## Installation
#### From the `/home/user` directory:
###### (or the same location as your `nhl-led-scoreboard` directory)

__Be sure to back up any previous configurations before use!!!__ The original files are overwritten and saved as `config.json.webgui.bak` and `config.schema.json.webgui.bak` in the `nhl-led-scoreboard/config/bak` subdirectory.

```
git clone --recursive https://github.com/sflems/nhl-led-scoreboard-webgui.git
cd nhl-led-scoreboard-webgui
./install.sh
python3 manage.py runserver 0:9002 --noreload
```
If all is working, you should then be able to access the app @ `YOUR_PI_IP:9002` in the browser. 

If you can't access the server and are using a firewall such as `ufw` or `iptables`, be sure to allow access _to your local network only_ over the `9002` port (or whatever you set it to if so). If you have ports 80/443 open on your Pi/Router, this site WILL be accessable by all, so be sure to have your firewall(s) in order. 
_____________

#### Optional but Suggested: 
###### Install `virtualenv` using `pip3`, create and activate the environment:

To run the server in a development environment, or if you have issues with dependencies, `virtualenv` can be a solution to create a separate "environment" for the server to run in.
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
```
_____________

## Screenshots
##### It's Mobile Freindly Too! (Responsive)
###### Dashboard
  <img src="/assets/images/LED Scoreboard Configurator - Dashboard.png" alt="LED Scoreboard Configurator - Dashboard" width="100%"/>
  
###### Profiles Dashboard
  <img src="/assets/images/LED Scoreboard Configurator - Profiles Dashboard.png" alt="LED Scoreboard Configurator - Profiles Dashboard" width="100%"/>
  
###### Create/Edit A Profile
  <img src="/assets/images/LED Scoreboard Configurator - Create_Edit A Profile.png" alt="LED Scoreboard Configurator - Create_Edit A Profile" width="100%"/>
  
###### Settings Admin
  <img src="/assets/images/LED Scoreboard Configurator - Settings Admin.png" alt="LED Scoreboard Configurator - Settings Admin" width="100%"/>

_____________

### Manual Installation:
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

_____________

## Usage
__Be sure to back up any previous configurations before use!!!__
#### To start the webserver:

To start the server, enter `python3 manage.py runserver 0:9002 --noreload` in your console from the directory that you installed the app in.
You can also run `./autorun.sh` from the same location.

This command, and the default configuration, start the server on `0.0.0.0` and port `9002` making it available to any connected devices on your local network. Alternatively, you can run the server on a different port, e.g. `0:8000`, `0:PORT`, or available to _just_ the `localhost` machine by running `python3 manage.py runserver --noreload`.

__Note__: *This feature is for local/development use only. It should not be served over a public connection or used in a production environment. If you wish to view the scoreboard WebGUI remotely, you can do so securely by accessing your local network using a VPN service.*

_____________

### To access the server:
_Access the dashboard at `YOUR_PI_IP:PORT` in the browser._

_____________

#### Auto-Starting the server @ boot: 
###### Create a script and use `rc.local` to autostart the devserver on startup:
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

${DIR}/env/bin/python3 ${DIR}/manage.py runserver 0:9002 --noreload &

exit 0
```

Alternatively, you can setup a [crontab](https://www.raspberrypi.org/documentation/linux/usage/cron.md), [systemd](https://www.raspberrypi.org/documentation/linux/usage/systemd.md), or another method of your choice to autostart the app.

_____________

### To stop the server:
In a terminal with the server running, `Ctrl` + `C` will terminate the process.

##### If the server is running in the background:
Enter `ps aux | grep runserver` and look for the process ID, or `PID` it returns for `/usr/bin/python3 manage.py runserver 0:9002`.

Example response:
```
    user@raspi:~ $ ps aux | grep runserver
--> user      6300 26.6  0.8  38236 33364 pts/0    S+   00:22   0:01 python3 manage.py runserver 0:9002
    user      6319  0.0  0.0   3160  1536 pts/1    S+   00:22   0:00 grep --color=auto runserver
    user@raspi:~ $ 
```
This is the second number in the table following the username (Use caution if you have more than one python/Django server running!). Change the `PID` in the following command to that number to kill the server:

`kill -9 PID`, or `pkill -f runserver` if you'd like to skip the step above.

Better yet... simply stop the server from the dashboard :).

_____________

#### Default Admin Login

`YOUR_PI_IP:9002/admin`

Username: `admin`

Password: `scoreboard`

__Please change this password!__ You can do this by visiting `YOUR IP:PORT/admin` and clicking the change password button. Email currently isn't configured.

_____________

#### Info
When a config is activated, the config.json contents are replaced with an updated configuration. You can do this on the profiles page. Your previous config.json is still "active" until you active one here.

When a profile is backed up, a file is created in the same folder as profile.config.json.bak. It's path is displayed as a message in the browser. Deleted profiles do not delete the config.json or .bak files; it only removes them from the Django Sqlite database. 

Speaking of which... _did you back up your profiles?_ ;)

### Please let me know if you experience any bugs, feature suggestions or issues. Enjoy!
