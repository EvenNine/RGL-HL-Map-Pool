import requests
import json
import os.path
import sys
from configparser import ConfigParser
import shutil

Config = open("config.ini", "w")

check_file = os.path.isfile("config.ini")
if check_file == True:
    print("config.ini has been created")

    Config.write("#Saved figure for previous RGL season" + "\n" +
    "[Current_RGL_Settings]" + "\n" +
    "hl_previous_season = 144" + "\n" +
    "Season = 147" + "\n" +
    "sixes_previous_season = 145" + "\n" +
    "sixes_season = 148" + "\n" +
    "Refrence_Team= Free Agent - Invite" + "\n"
    "#this is the server that maps will be downloaded from" + "\n" +
    "[Network]" + "\n" +
    "Fast_DL_Server_URL = https://fastdl.serveme.tf/maps/"  + "\n" +
    "\n"
    "[Log]" + "\n" +
    "default_map_location = /etc/" + "\n" +
    "log_file_directory = log.txt" + "\n" +
    "sixes_log_file_directory= 6slog.txt" + "\n")



    Config.close()
    print("Default config file has been built")

else:
    print("unable to create the config file")

