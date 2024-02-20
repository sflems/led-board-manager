#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3 15
exec 1>webgui-log.out 2>&1
#set -e
# Successful actions performed below will print to the terminal, else errors print to file 'webgui-log.out'.

# Gets the current working dir. 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# TARGET="$( cd "${DIR}/../../nhl-led-scoreboard" && pwd )" 
WORKING="$( cd "${DIR}/.." && pwd )"
echo "$(tput bold)Working directory:$(tput sgr0) "$WORKING >&3 && cd ${WORKING}

# Modify the nhl-led-scoreboard source to inject Stonks
echo "Getting installer requirements..." >&3
env/bin/python3 -m pip install inquirer
env/bin/python3 scripts/install_modify.py >&3

# A permission issue in the past was solved by creating the file on install and granting the permissions.
# The .secret.txt file is automatically generated and saved here. It may also need to have the appropriate write permissions as well.
echo "Touching .secret.txt and updating permissions..." >&3
touch .secret.txt >&3 && chmod g+w .secret.txt >&3 && echo "SUCCESS: Created and updated .secret.txt" >&3 || { echo "$(tput bold)$(tput setaf 1)ERROR: $(tput setaf 7)Unable to create .secret.txt. Check webgui-log.out for details." >&3; exit 1; }

# Install the app requirements and dependencies from the included requirements.txt file:
echo "Installing WebGUI requirements.txt. This may take a few moments..." >&3
if env/bin/python3 -m pip install --upgrade pip setuptools  >&3 && env/bin/python3 -m pip install --ignore-installed -r requirements.txt >&3; then
    echo "...done. " >&3
else
    echo "...$(tput bold)$(tput setaf 1)FAILED. " >&3
    exit 1
fi

# Create Django DB, load default data and run tests.
echo "Generating WebGUI database and loading initial data..." >&3

if ! [ env/bin/python3 manage.py makemigrations >&3 && env/bin/python3 manage.py migrate >&3 ]; then
    echo "...$(tput bold)$(tput setaf 1)FAILED. " >&3
    exit 1
fi

env/bin/python3 manage.py loaddata teams.json >&3 || echo "...$(tput bold)$(tput setaf 3)IMPORT ISSUE: See webgui-log.out for details. This can happen if you have an existing DB.$(tput setaf 7)$(tput sgr0)" >&3 # Ignores possible import issues. ie admin or profiles exist

if ! env/bin/python3 manage.py collectstatic --noinput; then
    echo "...$(tput bold)$(tput setaf 1)FAILED. " >&3
    exit 1
fi

if sudo ln -s /home/$USER/led-board-manager/supervisor-daemon.conf /etc/supervisor/conf.d/boardmanager.conf >&3; then
    echo "...done. " >&3
else
    sudo rm /etc/supervisor/conf.d/boardmanager.conf
    if sudo ln -s /home/$USER/led-board-manager/supervisor-daemon.conf /etc/supervisor/conf.d/boardmanager.conf >&3; then
        echo "...done. " >&3
    else
        echo "...$(tput bold)$(tput setaf 1)FAILED. " >&3
        exit 1
    fi
fi

echo "Running Django tests..." >&3
if env/bin/python3 manage.py test  >&3; then
    echo "...done. " >&3
else
    echo "...$(tput bold)$(tput setaf 1)FAILED. " >&3
    exit 1
fi

echo "Updating program configurations" >&3

if sudo supervisorctl update; then
    echo "...done. " >&3
else
    echo "...$(tput bold)$(tput setaf 1)FAILED. " >&3
    exit 1
fi

# Yay!?
echo "$(tput bold)No failures? SETUP COMPLETED!!!" >&3
echo "$(tput bold)Supervisor: $(tput sgr0)http://$(hostname -I | awk '{print $1}'):9001" >&3
echo "$(tput bold)LED Board Manager: $(tput sgr0)http://$(hostname -I | awk '{print $1}'):9002" >&3

exit 0
