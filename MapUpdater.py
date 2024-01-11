import requests
import json
import os.path
import requests
import sys
from configparser import ConfigParser
import shutil

config = ConfigParser()

#check if config file exists
check_file = os.path.isfile("config.ini")
if check_file == False:
    #load config.ini
    file = 'config.ini'
    file_open = open("config.ini", "w")
    config.read(file)

    print("config.ini does not exest, creating a new version with default settings..." + "\n")

    check_file = os.path.isfile("config.ini")
    if check_file == True:
        print("config.ini has been created")
        file_open.write("#Saved figure for previous RGL season" + "\n" +
        "[Current_RGL_Settings]" + "\n" +
        "Previous_Season = 144" + "\n" +
        "Season= 144" + "\n" +
        "Refrence_Team= Free Agent - Invite" + "\n" + "\n" +

        "#this is the server that maps will be downloaded from" + "\n" +
        "[Network]" + "\n" +
        "Fast_DL_Server_URL = https://fastdl.serveme.tf/maps/"  + "\n" +
        "\n"
        "[Log]" + "\n" +
        "default_map_location = /etc/" + "\n" +
        "log_file_directory = log.txt" + "\n")

        file_open.close()
        print("A new config file has been created please update the config.ini file with your tf/maps/ file location")
        exit()


    else:
        print("unable to create config.ini")

else:
    print("Config.ini has been found, loading." + "\n")




#load config.ini
file = 'config.ini'
config = ConfigParser()
config.read(file)

# output files to log
sys.stdout = open(config['Log']['log_file_directory'], 'w')

#check if a new season exists
Latest_RGL_Season = config['Current_RGL_Settings']['Season']
Previous_season_CFG = config['Current_RGL_Settings']['previous_season']

##Get latest team ID for team designated in config.ini
headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
}

params = {
    'take': '100',
    'skip': '0',
}

json_data = {
    'nameContains': config['Current_RGL_Settings']['Refrence_Team'],
}

Refrence_Team_Alias_Pull = requests.post('https://api.rgl.gg/v0/search/teams', params=params, headers=headers, json=json_data)

##after pulling the information the data now is parsed to pull the latest team ID
rgl_api_parse = json.loads(Refrence_Team_Alias_Pull.text)
rgl_team_id = rgl_api_parse['results']
RGL_Team_ID_Latest = ''.join(rgl_team_id[-1:])
print ("Most recent team ID for " + str(config['Current_RGL_Settings']['Refrence_Team']) + "is : " + RGL_Team_ID_Latest)


##The team ID is then added to the team search URL.
RGL_API_Team_Search_URL = "https://api.rgl.gg/v0/teams/" + RGL_Team_ID_Latest


## This URL is then Parsed in order to get the latest Season ID this is required to make sure you are pulling the map pool from the correct season.
RGL_API_Team_Search = requests.get(RGL_API_Team_Search_URL, headers=headers)
rgl_api_parse = json.loads(RGL_API_Team_Search.text)
RGL_Season_ID = rgl_api_parse['seasonId']

print("\n")
print("The current season ID is : "  + str(RGL_Season_ID) + " Previous is: " + config['Current_RGL_Settings']['Season'] + "\n")


##We now need to update the config file


if str(RGL_Season_ID) > Latest_RGL_Season:
    print("updating config to newest season")
    config.set( 'Current_RGL_Settings', 'Previous_Season', str(Latest_RGL_Season) )
    config.set ( 'Current_RGL_Settings', 'Season', str(RGL_Season_ID) )

    with open(file, 'w') as configfile:
        config.write(configfile)

else:
    print("Config file does not need to be updated." "\n")



RGL_Latest_map_check = str(RGL_Season_ID)

#Request Maps from RGL API
RGL_API_URL = "https://api.rgl.gg/v0/seasons/" + RGL_Latest_map_check
response_API = requests.get(RGL_API_URL)
data = response_API.text
parse_json = json.loads(data)
RGL_Current_Maps = parse_json['maps']
RGL_map_check = ''.join(RGL_Current_Maps[-1:])

if RGL_map_check == '':
    print("Season " + str(RGL_Season_ID) + " does not have any maps posted, pulling maps from previously used Season " + Previous_season_CFG + "\n")
    RGL_Season_ID = str(Previous_season_CFG)

else:
    print(RGL_map_check)
    print("Season " + str(RGL_Season_ID) + " has maps, checking for updates" + "\n")









#Set RGL season ID (place holder for quereing the season ID) set to S 144 Season 16 HL

#RGL_Season_ID = "144"

#Request Maps from RGL API
RGL_API_URL = "https://api.rgl.gg/v0/seasons/" + str(RGL_Season_ID)
response_API = requests.get(RGL_API_URL)
data = response_API.text
parse_json = json.loads(data)
RGL_Current_Maps = parse_json['maps']

##output the maps that are being played in the season
print("Current maps in rotation : " + "\n")
for Season_map in RGL_Current_Maps:
    print(" " + Season_map)

print("\n + Downloading maps..."+ "\n")

#Download the maps
Fast_DL_Server_URL = config['Network']['Fast_DL_Server_URL']


Server_Map_folder = config['Log']['default_map_location']

###It will now look in the designated tf2 maps folder to see if the maps are present
for Season_map in RGL_Current_Maps:
    Map_DL_link = Fast_DL_Server_URL + Season_map + ".bsp"
    Map_Name = Season_map + ".bsp"

    Server_Map_folder_file = Server_Map_folder + Map_Name
    check_file = os.path.isfile(Server_Map_folder_file)

    if check_file == False:

        print (Map_Name + " does not exist, downloading  ")
        Server_Map_folder_file = Server_Map_folder + Map_Name

        response = requests.get(Map_DL_link)

        with open(Map_Name, 'wb') as f:
            f.write(response.content)
        shutil.move(Map_Name, Server_Map_folder_file)


        print ("File " + Map_Name + " has been downloaded from " + Map_DL_link)
        print(Map_Name + " has been moved to " + Server_Map_folder_file + "\n")

    else:
        print(Map_Name + " is already present, skipping download" + "\n" )

sys.stdout.close()
