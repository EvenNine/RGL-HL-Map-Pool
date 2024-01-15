import requests
import json
import os.path
import requests
import sys
from configparser import ConfigParser
import shutil
import subprocess


config = ConfigParser()

#check if config file exists
check_file = os.path.isfile("config.ini")
if check_file == False:

    with open("Build_Config.py") as f:
        exec(f.read())

    print("Please update the Config. ini file with dl location")


else:
    print("Config.ini has been found, loading." + "\n")



subprocess.run(["python3", "sixslookup.py"])
subprocess.run(["python3", "maplookup.py"])
