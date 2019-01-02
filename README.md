# Absence.io time tracker helper

## Install
- `git clone`
- run `pip --user install -r requirements.txt`
- change the following in `track.py` with your absence.io API credentials
 
````
user_id = "<user_id>"
key = "<api_key>"
timezoneName = "CET"
timezone = "+0100"
````

## Run
- run `python3 track.py start` to start tracking
- run `python3 track.py stop` to stop tracking