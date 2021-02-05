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

echo "Changing autorun.sh and .secret.txt permissions..." 1>&3
# The autorun script needs permission to start the server.
chmod +x autorun.sh

# The .secret.txt file is automatically generated and saved here. It may also need to have the appropriate write permissions as well.
touch .secret.txt
chmod g+w .secret.txt

# Install the app requirements and dependencies from the included requirements.txt file:
pip3 install -r requirements.txt

echo "Moving original config.json and schema files to "$TARGET"/config/bak/original/" 1>&3

mkdir -p $TARGET/config/bak/original

# Copy the updated Schema and default config to the config folder in the nhl-led-scoreboard directory. Backs up originals first.
mv $TARGET/config/config.json $TARGET/config/bak/original/config.json
mv $TARGET/config/config.schema.json $TARGET/config/bak/original/config.schema.json

echo "Updating schema with modified version..." 1>&3

cp ./scoreboard/fixtures/config.json $TARGET/config/config.json
cp ./scoreboard/static/schema/config.schema.json $TARGET/config/config.schema.json

echo "Generating WebGUI database and loading initial data..." 1>&3

# Create Django DB and load default data.
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata teams.json


echo "Starting server on: 0.0.0.0:9002. Access on your local network @ http://YOURIP:9002" 1>&3


# Start server on localhost
python3 manage.py runserver 0:9002 --noreload & 1>&3

echo "Setup completed." 1>&3
exit 0
