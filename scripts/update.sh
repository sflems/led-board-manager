#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3 15
exec 1>webgui-log.out 2>&1
set -e
# Successful actions performed below will print to the terminal, else errors print to file 'webgui-log.out'.

# Gets the current working dir. 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
WORKING="$( cd "${DIR}/.." && pwd )"
echo "$(tput bold)Working directory:$(tput sgr0) "$WORKING >&3 && cd ${WORKING}

# Install the app requirements and dependencies from the included requirements.txt file:
echo "Installing WebGUI requirements.txt. This may take a few moments..." >&3
env/bin/python3 -m pip install -U -r requirements.txt >&3

# Create Django DB, load default data, and run tests.
echo "Updating WebGUI database and loading initial data..." >&3
env/bin/python3 manage.py makemigrations >&3 || echo "...FAILED. " >&3
env/bin/python3 manage.py migrate >&3 || echo "...FAILED. " >&3
env/bin/python3 manage.py loaddata teams.json >&3 ||

echo "Running Django tests..." >&3
env/bin/python3 manage.py test >&3 && echo "...done. " >&3 || echo "...FAILED. " >&3

echo "Updating supervisor configurations..." >&3
sudo supervisorctl reread >&3 && echo "...(1/3) - done. " >&3 || echo "...(1/3) - FAILED. " >&3
sudo supervisorctl reload >&3 && echo "...(2/3) - done. " >&3 || echo "...(2/3) - FAILED. " >&3
echo "Updating program configurations" >&3
sleep 3 && sudo supervisorctl update >&3 && echo "...(3/3) - done. " >&3 || echo "...(3/3) - FAILED. " >&3

echo "$(tput bold)No failures? UPDATE COMPLETED!!!" >&3
echo "$(tput sgr0)Start the Web GUI server with $(tput bold)'source env/bin/activate && gunicorn Capstone.wsgi -b 0:9002'$(tput sgr0) or $(tput bold)'./scripts/autorun.sh'$(tput sgr0)" >&3

exit 0