#!/usr/bin/env python3

import os.path
import inquirer
import shutil
import json

cwd = os.path.os.getcwd()

# Verify the path
def path_verify(path):
    if path[-1] == '/':
        path = path[0:-1]
    if not os.path.isdir(path):
        print(f"\nERROR: Supplied path does not exist - {path}")
        quit()
    return path

# Prompt for additional boards
questions = [
  inquirer.Checkbox('boards',
                    message="Select additional boards (use space to select)",
                    choices=['MLB-LED-Scoreboard', 'NFL-LED-Scoreboard'],
                ),
]
answers = inquirer.prompt(questions)

if "MLB-LED-Scoreboard" in answers["boards"]:
    print('')
    print('Enter the full path to `MLB-LED-Scoreboard`. ')
    mlb_path = input('Leave blank for "/home/pi/mlb-led-scoreboard": ')
    if mlb_path == "":
        mlb_path = "/home/pi/mlb-led-scoreboard"
    else:
        path_verify(mlb_path)
    print(f"INFO: Working path is: {mlb_path}\n")

    # Copy MLB schema to working directory.
    print(f"Copying 'mlb.config.schema.json' to `{mlb_path}`... ", end='')
    shutil.copyfile(f'{cwd}/scoreboard/static/schema/mlb.config.schema.json',f"{mlb_path}/config.schema.json")
    print("done.")

if "NFL-LED-Scoreboard" in answers["boards"]:
    print('')
    print('Enter the full path to `NFL-LED-Scoreboard`. ')
    nfl_path = input('Leave blank for "/home/pi/nfl-led-scoreboard": ')
    if nfl_path == "": 
        nfl_path = "/home/pi/nfl-led-scoreboard"
    else:
        path_verify(nfl_path)
    print(f"INFO: Working path is: {nfl_path}\n")

    # Copy MLB schema to working directory.
    print(f"Copying 'nfl.config.schema.json' to `{nfl_path}`... ", end='')
    shutil.copyfile(f'{cwd}/scoreboard/static/schema/nfl.config.schema.json', f"{nfl_path}/config.schema.json")
    print("done.")