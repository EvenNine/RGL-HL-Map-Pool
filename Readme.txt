To install and run the script with python, the script will create a file named log.txt and config.ini. Set your tf/maps file before running the file. 
if you have issues with the config.ini file you can just delete it and the script will rebuild it with default settings.
Log.txt contains the log from the previous run. 

MapUpdater.py downloads the current map pool by querying the RGL API for a specific team, by base Free Agent - Invite. 
The script then pulls the latest season ID for the selected team.
it will then compare the season the script saved in config.ini and update the season, and previous season. it does this in case the script is run before the RGL maps are posted
The script will then check your designated maps/tf folder to see if the maps currently exist. If the map exists it will skip download. 
