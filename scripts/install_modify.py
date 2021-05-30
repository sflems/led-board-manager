#!/usr/bin/env python3

import os.path
import inquirer
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
print('\nEnter the full path to `NHL-LED-Scoreboard`. ')
nhl_path = input(print('Leave blank for "/home/pi/nhl-led-scoreboard": '))

if nhl_path == "":
    nhl_path = "/home/pi/nhl-led-scoreboard"
else:
    nhl_path = path_verify(nhl_path)
    new_file = []

with open(cwd + "/Capstone/settings.py", 'r') as f:
    for line in f.read():
        if not "NHL_SCOREBOARD_PATH =" in line:
            new_file.append(line)
        else:
            line = 'NHL_SCOREBOARD_PATH = "{}"'.format(nhl_path)
            new_file.append(line)
    f.close()

with open(cwd + "/Capstone/settings.py", 'w') as f:
    for line in new_file:
        f.write(line)
    f.close()

print(f"INFO: NHL scoreboard path has been configured to: `{nhl_path}`.\n")

# Prompt for additional boards
questions = [
  inquirer.Checkbox('boards',
                    message="Select additional boards (use space to select)",
                    choices=['MLB-LED-Scoreboard', 'NFL-LED-Scoreboard'],
                ),
]
answers = inquirer.prompt(questions)

if "MLB-LED-Scoreboard" in answers["boards"]:
    print('Enter the full path to `MLB-LED-Scoreboard`. ')
    mlb_path = input(print('Leave blank for "/home/pi/mlb-led-scoreboard": '))
    if mlb_path == "":
        mlb_path = "/home/pi/mlb-led-scoreboard"
    else:
        mlb_path = path_verify(mlb_path)
    print(f"INFO: Working path is: {mlb_path}")

    # Copy MLB schema to working directory.
    print(f"Copying 'mlb.config.schema.json' to `{mlb_path}`... ", end='')
    shutil.copyfile(
        f'{cwd}/scoreboard/static/schema/mlb.config.schema.json',
        f"{mlb_path}/config.schema.json"
    )
    print("done.\n")

if "NFL-LED-Scoreboard" in answers["boards"]:
    print('Enter the full path to `NFL-LED-Scoreboard`. ')
    nfl_path = input(print('Leave blank for "/home/pi/nfl-led-scoreboard": '))
    if nfl_path == "":
        nfl_path = "/home/pi/nfl-led-scoreboard"
    else:
        nfl_path = path_verify(nfl_path)
    print(f"INFO: Working path is: {nfl_path}")

    # Copy MLB schema to working directory.
    print(f"Copying 'nfl.config.schema.json' to `{nfl_path}`... ", end='')
    shutil.copyfile(
        f'{cwd}/scoreboard/static/schema/nfl.config.schema.json',
        f"{nfl_path}/config.schema.json"
    )
    print("done.\n")
