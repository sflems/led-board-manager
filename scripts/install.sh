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
echo "Getting installer requirements..." >&3
env/bin/python3 -m pip install inquirer >&3
env/bin/python3 scripts/install_modify.py >&3

# A permission issue in the past was solved by creating the file on install and granting the permissions.
# The .secret.txt file is automatically generated and saved here. It may also need to have the appropriate write permissions as well.
echo "Touching .secret.txt and updating permissions..." >&3
touch .secret.txt >&3 && chmod g+w .secret.txt >&3 && echo "SUCCESS: Created and updated .secret.txt" >&3 || { echo "ERROR: Unable to create .secret.txt. Check webgui-log.out for details." >&3; exit 1; }

# Install the app requirements and dependencies from the included requirements.txt file:
echo "Installing WebGUI requirements.txt. This may take a few moments..." >&3
env/bin/python3 -m pip install --upgrade pip >&3
env/bin/python3 -m pip install --upgrade setuptools >&3
env/bin/python3 -m pip install --ignore-installed -r requirements.txt >&3

# Create Django DB, load default data and run tests.
echo "Generating WebGUI database and loading initial data..." >&3
env/bin/python3 manage.py makemigrations >&3 || echo "...FAILED. " >&3
env/bin/python3 manage.py migrate >&3 || echo "...FAILED. " >&3
env/bin/python3 manage.py loaddata teams.json >&3 # Ignores possible import issues. ie admin or profiles exist
env/bin/python3 manage.py collectstatic >&3 || echo "...FAILED. " >&3

echo "Running Django tests..." >&3
env/bin/python3 manage.py test >&3 && echo "...done. " >&3 || echo "...FAILED. " >&3

echo "Updating supervisor configurations..." >&3
sudo supervisorctl reread >&3 && echo "...(1/3) - done. " >&3 || echo "...(1/3) - FAILED. " >&3
sudo supervisorctl reload >&3 && echo "...(2/3) - done. " >&3 || echo "...(2/3) - FAILED. " >&3
echo "Updating program configurations" >&3
sleep 3 && sudo supervisorctl update >&3 && echo "...(3/3) - done. " >&3 || echo "...(3/3) - FAILED. " >&3

# Yay!?
echo "$(tput bold)No failures? SETUP COMPLETED!!!" >&3
echo "$(tput sgr0)Start the Web GUI server with $(tput bold)'source env/bin/activate && gunicorn Capstone.wsgi -b 0:9002'$(tput sgr0) or $(tput bold)'./scripts/autorun.sh'$(tput sgr0)" >&3

exit 0
