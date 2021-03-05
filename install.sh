#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3 15
exec 1>webgui-log.out 2>&1
set -e
# Successful actions performed below will print to the terminal, else errors print to file 'webgui-log.out'.

# Gets the current working dir. 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TARGET="$( cd ../nhl-led-scoreboard && pwd )"
echo "Working directory: "$DIR >&3
echo "Target: "$TARGET >&3

cd $DIR

# A permission issue in the past was solved by creating the file on install and granting the permissions.
echo "Touching .secret.txt and updating permissions..." >&3

# The .secret.txt file is automatically generated and saved here. It may also need to have the appropriate write permissions as well.
touch .secret.txt >&3 && chmod g+w .secret.txt >&3 && echo "SUCCESS: Created and updated .secret.txt" >&3 || { echo "ERROR: Unable to create .secret.txt. Check webgui-log.out for details." >&3; exit 1; }

# Start the venv
source env/bin/activate >&3

# Install the app requirements and dependencies from the included requirements.txt file:
echo "Installing requirements.txt. This may take a few moments..." >&3
python3 -m pip install --ignore-installed -r requirements.txt >&3

echo "Generating WebGUI database and loading initial data..." >&3

# Create Django DB and load default data.
env/bin/python3 manage.py makemigrations >&3
env/bin/python3 manage.py migrate >&3
env/bin/python3 manage.py loaddata teams.json >&3

echo "SETUP COMPLETED!!!" >&3
echo "Start the Web GUI server with 'gunicorn Capstone.wsgi -b 0:9002' or './autorun.sh'" >&3

exit 0
