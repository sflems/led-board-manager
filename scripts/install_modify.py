#!/usr/bin/env python3

import os.path
import inquirer
import json
import shutil
import sys

cwd = os.path.os.getcwd()
sys.path.append(cwd)


# Verify the path
def path_verify(path):
    if path[-1] == '/':
        path = path[0:-1]
    if not os.path.isdir(path):
        print(f"\nWARNING: Supplied path does not exist - {path}. Skipping...")
        quit()
    return path

# Ask user for the directory to the nhl-led-scoreboard path
print('\nEnter the full path to `NHL-LED-Scoreboard`. (Must contain "nhl".) ')
nhl_path = input(print('Leave blank for "/home/pi/nhl-led-scoreboard": '))

if nhl_path == "":
    nhl_path = path_verify("/home/pi/nhl-led-scoreboard")
else:
    nhl_path = path_verify(nhl_path)

# Update Capstone/settings.py with scoreboard path.
new_file = []
with open(cwd + "/Capstone/settings.py", 'r') as f:
    for line in f:
        if "NHL_SCOREBOARD_PATH = " in line:
            line = 'NHL_SCOREBOARD_PATH = "{}"\n'.format(nhl_path)
            new_file.append(line)
        elif "GUI_PATH = " in line:
            line = 'GUI_PATH = "{}"\n'.format(cwd)
            new_file.append(line)
        else:
            new_file.append(line)
    f.close()

with open(cwd + "/Capstone/settings.py", 'w') as f:
    output = "".join(new_file)
    f.write(output)
    f.close()

with open(f"{cwd}/scoreboard/fixtures/teams.json", "r") as f:
    loading_data = json.load(f)
    for item in loading_data:
        if "pk" in item.keys() and item['pk'] == "NHL":
            item['fields']['path'] = nhl_path

with open(f"{cwd}/scoreboard/fixtures/teams.json", "w") as json_out:
    json.dump(loading_data, json_out, indent=2)
    json_out.close()

print(f"INFO: Capstone.settings.NHL_SCOREBOARD_PATH has been configured to: `{nhl_path}`.")
print(f"INFO: Capstone.settings.GUI_PATH has been configured to: `{cwd}`.\n")

# Prompt for additional boards
questions = [
  inquirer.Checkbox('boards',
                    message="Select additional boards (use space to select)",
                    choices=['MLB-LED-Scoreboard', 'NFL-LED-Scoreboard'],
                ),
]
answers = inquirer.prompt(questions)

# Update MLB BoardType.path
if "MLB-LED-Scoreboard" in answers["boards"]:
    print('Enter the full path to `MLB-LED-Scoreboard`. ')
    mlb_path = input(print('Leave blank for "/home/pi/mlb-led-scoreboard": '))
    if mlb_path == "":
        mlb_path = "/home/pi/mlb-led-scoreboard"
    else:
        mlb_path = path_verify(mlb_path)
    print(f"INFO: MLB BoardType.path has been configured to: `{mlb_path}`.")
    
    with open(f"{cwd}/scoreboard/fixtures/teams.json", "r") as f:
        loading_data = json.load(f)
        for item in loading_data:
            if "pk" in item.keys() and item['pk'] == "MLB":
                item['fields']['path'] = mlb_path

    with open(f"{cwd}/scoreboard/fixtures/teams.json", "w") as json_out:
        json.dump(loading_data, json_out, indent=2)
        json_out.close()

    # Copy MLB schema to working directory.
    print(f"Copying 'mlb.config.schema.json' to `{mlb_path}`... ", end='')
    shutil.copyfile(
        f'{cwd}/scoreboard/static/schema/mlb.config.schema.json',
        f"{mlb_path}/config.schema.json"
    )
    print("done.\n")

# Update NFL BoardType.path
if "NFL-LED-Scoreboard" in answers["boards"]:
    print('Enter the full path to `NFL-LED-Scoreboard`. ')
    nfl_path = input(print('Leave blank for "/home/pi/nfl-led-scoreboard": '))
    if nfl_path == "":
        nfl_path = "/home/pi/nfl-led-scoreboard"
    else:
        nfl_path = path_verify(nfl_path)
    print(f"INFO: NFL BoardType.path has been configured to: `{nfl_path}`.")

    with open(f"{cwd}/scoreboard/fixtures/teams.json", "r") as f:
        loading_data = json.load(f)
        for item in loading_data:
            if "pk" in item.keys() and item['pk'] == "NFL":
                item['fields']['path'] = nfl_path

    with open(f"{cwd}/scoreboard/fixtures/teams.json", "w") as json_out:
        json.dump(loading_data, json_out, indent=2)
        json_out.close()

    # Copy MLB schema to working directory.
    print(f"Copying 'nfl.config.schema.json' to `{nfl_path}`... ", end='')
    shutil.copyfile(
        f'{cwd}/scoreboard/static/schema/nfl.config.schema.json',
        f"{nfl_path}/config.schema.json"
    )
    print("done.\n")
