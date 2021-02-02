# NHL LED Scoreboard Web GUI & Configurator
#### A Django based web app to configure an <a href="https://github.com/riffnshred/nhl-led-scoreboard">NHL LED Scoreboard</a> running on a Raspberry Pi.
_(Work in Progress)_

## Requirements

- [Hockey](https//www.nhl.com)

- [App Dependancies](requirements.txt)

## Installation
#### From the `/home/user` directory:
###### (or in the same location as your `nhl-led-scoreboard` directory)
```
git clone -r https://github.com/sflems/nhl-led-scoreboard-WebGUI.git
cd nhl-led-scoreboard-WebGUI
su
chmod -x autorun.sh
chmod g-x .secret.txt
su (username)
```

#### Optional but Suggested: 
###### Install `virtualenv` using `pip3`, create and activate the environment:

To run the server in a development environment, or if you have issues with dependencies, `virtualenv` can be a solution to create a separate "environment" for the server to run in.
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
```

#### Install the app requirements and dependencies from the included requirements.txt file:
`pip3 install -r requirements`

#### Once complete, we'll make, migrate and fill our sqlite3 database with the supplied teams data in the fixtures folder:

First, run:

`python3 manage.py makemigrations`.

Followed by:

`python3 manage.py migrate`.

And lastly:

`python3 manage.py loaddata teams.json`



#### Finally we'll fire up the devserver from Django to test out our install:

To start the server, enter `python3 manage.py runserver 0:9002` in your console from the directory that you installed the app in.
You can also run `./autorun.sh` from the same location.

This command, and the default configuration, start the server on `0.0.0.0` and port `9002` making it available to any connected devices on your local network. Alternatively, you can run the server on a different port, e.g. `0:8000`, `0:PORT`, or available to _just_ the `localhost` machine by running `python3 manage.py runserver`.

__Note__: *This feature is for local/development use only. It should not be served over a public connection or used in a production environment. If you wish to view the scoreboard WebGUI remotely, you can do so securely by accessing your local network using a VPN service.*

#### Optional: 
##### Create a script and us `rc.local` to autostart the devserver on startup:
We're going to use the Raspberry Pi's `/etc/rc.local` file to start our script at startup time. In the `/nhl-led-scoreboard-webGUI` folder, create a new file using:

`sudo nano autorun.sh` 

...and enter the following contents, substituting your username for `user`, or `pi` if it is still the default:

```
#!/bin/bash

cd /home/user/nhl-led-scoreboard-webGUI
source env/bin/activate
exec python3 /home/user/nhl-led-webGUI/manage.py runserver 0:9002 --noreload &

exit 0
```

Then we'll add this script to the Raspberry Pi's `/etc/rc.local` file.

Enter `sudo nano /etc/rc.local` to add the following line before `exit 0`:

```
su user -c '/home/user/nhl-led-scoreboard-webGUI/autorun.sh >> /tmp/scoreboard-gui.log 2>&1'
```
...again substituting your own username for `user`, or `pi` if it is still the default.

Alternatively, you can setup a [crontab](https://www.raspberrypi.org/documentation/linux/usage/cron.md), [systemd](https://www.raspberrypi.org/documentation/linux/usage/systemd.md), or another method of your choice to autostart the app.

#### To stop the server:
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
This is the second number in the table following the username (Use caution if you have more than one python/Django server running!). Use the PID in the following command to kill the server:

`kill -9 PID` 

Or... simply stop the server from the dashboard in the following steps :).

## Usage

Default Admin Login: `admin`

Default Admin Password: `scoreboard`
