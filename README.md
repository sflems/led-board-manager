# NHL LED Scoreboard Web GUI & Configurator
#### A Django based web app to configure an <a href="https://github.com/riffnshred/nhl-led-scoreboard">NHL LED Scoreboard</a> running on a Raspberry Pi.

Designed as a solution to manage the NHL LED Scoreboard project by [Joel Joannisse](https://github.com/riffnshred). 

The app uses the current configuration schema found in the `nhl-led-scoreboard/config` directory and generates a form to modify the config. At the moment, configurations you edit are validated against this current schema exclusively. I'd certainly like to get cross version editing working sooner than later.

_(Work in Progress)_

## Requirements

- [Hockey](https//www.nhl.com)

- [App Dependancies](requirements.txt)

## Installation
#### From the `/home/user` directory:
###### (or the same location as your `nhl-led-scoreboard` directory)
__Be sure to back up any previous configurations before use!!!__
The original files are overwritten and saved as `config.json.webgui.bak` and `config.schema.json.webgui.bak` in the `nhl-led-scoreboard/config/bak` subdirectory.

```
git clone --recursive https://github.com/sflems/nhl-led-scoreboard-webgui.git
cd nhl-led-scoreboard-webgui
chmod +x install.sh
./install.sh
```
If all is working, you should then be able to access the app @ `YOUR_IP:9002` in the browser. 

If you can't access the server and are using a firewall such as `ufw` or `iptables`, be sure to allow access _to your local network only_ over the `9002` port (or whatever you set it to if so).
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

### Manual Installation:
```
chmod +x autorun.sh
chmod g+w .secret.txt
```

The autorun script needs permission to start the server. The .secret.txt file is automatically generated and saved here. It may also need to have the appropriate write permissions as well.


###### Install the app requirements and dependencies from the included requirements.txt file:
`pip3 install -r requirements`

###### Once complete, we'll make, migrate and fill our sqlite3 database with the supplied teams data in the fixtures folder:

First, run:

`python3 manage.py makemigrations`.

Followed by:

`python3 manage.py migrate`.

And lastly:

`python3 manage.py loaddata teams.json`


###### Finally we'll fire up the devserver from Django to test out our install:

To start the server, enter `python3 manage.py runserver 0:9002` in your console from the directory that you installed the app in.
You can also run `./autorun.sh` from the same location.

This command, and the default configuration, start the server on `0.0.0.0` and port `9002` making it available to any connected devices on your local network. Alternatively, you can run the server on a different port, e.g. `0:8000`, `0:PORT`, or available to _just_ the `localhost` machine by running `python3 manage.py runserver`.

__Note__: *This feature is for local/development use only. It should not be served over a public connection or used in a production environment. If you wish to view the scoreboard WebGUI remotely, you can do so securely by accessing your local network using a VPN service.*

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

${DIR}/env/bin/python3 ${DIR}/manage.py runserver 0:9002 --noreload &

exit 0
```

Alternatively, you can setup a [crontab](https://www.raspberrypi.org/documentation/linux/usage/cron.md), [systemd](https://www.raspberrypi.org/documentation/linux/usage/systemd.md), or another method of your choice to autostart the app.

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

`kill -9 PID` 

Or... simply stop the server from the dashboard in the following steps :).


## Usage
__Be sure to back up any previous configurations before use!!!__

Access the dashboard at `YOUR_IP:PORT` in the browser.

__Default Admin Login__


Username: `admin`

Password: `scoreboard`

__Please change this password!__ You can do this by visiting `YOUR IP:PORT/admin` and clicking the change password button. Email currently isn't configured.

When a config is activated, the config.json contents are replaced with an updated configuration. You can do this on the profiles page. 

When a profile is backed up, a file is created in the same folder as profile.config.json.bak. It's path is displayed as a message in the browser. Deleted profiles do not delete the config.json or .bak files; it only removes them from the Django Sqlite database. 

Speaking of which... _did you back up your profiles?_ ;)

### Please let me know if you experience any bugs or issues as this is still in the testing phase!
