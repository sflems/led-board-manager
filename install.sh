#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>log.out 2>&1
# Everything below will go to the file 'log.out':

# Gets the current working dir. 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}/.."

# The autorun script needs permission to start the server.
chmod +x autorun.sh

# The .secret.txt file is automatically generated and saved here. It may also need to have the appropriate write permissions as well.
chmod g+w .secret.txt

# Install the app requirements and dependencies from the included requirements.txt file:
pip3 install -r requirements

# Copy the updated Schema and default config to the config folder in the nhl-led-scoreboard directory. Backs up originals first.
mv ../nhl-led-scoreboard/config/config.json ../nhl-led-scoreboard/config/bak/config.json.webgui.bak 
mv ../nhl-led-scoreboard/config.scema.json ../nhl-led-scoreboard/config/bak/config.schema.json.webgui.bak

cp ./scoreboard/fixtures/config.json ../nhl-led-scoreboard/config/config.json
cp ./scoreboard/static/schema/config.schema.json ../nhl-led-scoreboard/config/config.schema.json

# Create Django DB and load default data.
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata teams.json

# Start server on 0.0.0.0
python3 manage.py runserver 0:9002 --noreload &

exit 0