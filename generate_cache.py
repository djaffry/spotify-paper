
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
from src import conf_helper
import os
import sys


def _is_running_on_RPi():
    rpidriver_path = Path("/sys/bus/platform/drivers/gpiomem-bcm2835")
    if rpidriver_path.is_dir() or rpidriver_path.is_file():
        return True
    return False


def _generate_chache():
    conf = conf_helper.get_config()
    cache_path = Path(".cache")

    if cache_path.is_file():
        print('Cache already generated. located in:', cache_path)
        return

    scope = "user-read-currently-playing, user-read-playback-state"
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyOAuth(
            client_id=conf['spotify']['client_id'], 
            client_secret=conf['spotify']['client_secret'], 
            redirect_uri=conf['spotify']['redirect_uri'], 
            scope=scope))
    sp.current_playback(additional_types='episode') # should generate .cache

    if cache_path.is_file():
        print('Cache generated. located in:', cache_path)
    else:
        print('ERROR: Cache could not be generated')



if _is_running_on_RPi():
    print('\nWARNING: You need a monitor and browser to generate the cache.')
    if not input("Continue? (y/n): ").lower().strip()[:1] == "y": sys.exit(1)

_generate_chache()
