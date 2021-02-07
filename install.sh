#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>webgui-log.out 2>&1
# Everything below will go to the file 'webgui-log.out':

# Gets the current working dir. 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TARGET="$( cd ../nhl-led-scoreboard && pwd )"
echo "Working directory: "$DIR 1>&3
echo "Target: "$TARGET 1>&3

# A permission issue in the past was solved by creating the file on install and granting the permissions.
echo "Creating and changing .secret.txt permissions..." 1>&3

# The .secret.txt file is automatically generated and saved here. It may also need to have the appropriate write permissions as well.
touch .secret.txt
chmod g+w .secret.txt

# Install the app requirements and dependencies from the included requirements.txt file:
pip3 install -r requirements.txt

echo "Moving original schema file to "$TARGET"/config/bak/original/" 1>&3

mkdir -p $TARGET/config/bak/original

# Copy the updated Schema to the config folder in the nhl-led-scoreboard directory. Backs up original first.
mv $TARGET/config/config.schema.json $TARGET/config/bak/original/$(date +"%Y_%m_%d_%I_%M_%p")-config.schema.json

echo "Updating schema with modified version..." 1>&3

# THIS NEEDS TO BE UPDATED FOR THE 2021-2022 Season!!! Updated schema file with divisions is in static/schema dir.
cp ./scoreboard/static/schema/config.schema.json $TARGET/config/config.schema.json

echo "Generating WebGUI database and loading initial data..." 1>&3

# Create Django DB and load default data.
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata teams.json

echo "Setup completed. Start the server with 'command python3 manage.py runserver 0:9002 --noreload &', or './autorun.sh'" 1>&3
exit 0
