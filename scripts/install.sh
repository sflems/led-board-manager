#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3 15
exec 1>webgui-log.out 2>&1
set -e
# Successful actions performed below will print to the terminal, else errors print to file 'webgui-log.out'.

# Gets the current working dir. 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# TARGET="$( cd "${DIR}/../../nhl-led-scoreboard" && pwd )" 
WORKING="$( cd "${DIR}/.." && pwd )"
echo "$(tput bold)Working directory:$(tput sgr0) "$WORKING >&3 && cd ${WORKING}

# Modify the nhl-led-scoreboard source to inject Stonks
env/bin/python3 -m pip install inquirer >&3
env/bin/python3 scripts/install_modify.py >&3

# A permission issue in the past was solved by creating the file on install and granting the permissions.
echo "Touching .secret.txt and updating permissions..." >&3

# The .secret.txt file is automatically generated and saved here. It may also need to have the appropriate write permissions as well.
touch .secret.txt >&3 && chmod g+w .secret.txt >&3 && echo "SUCCESS: Created and updated .secret.txt" >&3 || { echo "ERROR: Unable to create .secret.txt. Check webgui-log.out for details." >&3; exit 1; }

# Install the app requirements and dependencies from the included requirements.txt file:
echo "Installing requirements.txt. This may take a few moments..." >&3
env/bin/python3 -m pip install --ignore-installed -r requirements.txt >&3

# Create Django DB and load default data.
echo "Generating WebGUI database and loading initial data..." >&3
env/bin/python3 manage.py makemigrations >&3
env/bin/python3 manage.py migrate >&3
env/bin/python3 manage.py loaddata teams.json >&3

echo "$(tput bold)SETUP COMPLETED!!!" >&3
echo "Start the Web GUI server with $(tput bold)'source env/bin/activate && gunicorn Capstone.wsgi -b 0:9002'$(tput sgr0) or $(tput bold)'./autorun.sh'$(tput sgr0)" >&3

exit 0
