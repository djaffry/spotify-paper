
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

from . import bpm_render
from . import conf_helper

API_LATENCY_SECS = 1.5

def get_currently_playing():
	conf = conf_helper.get_config()

	scope = "user-read-currently-playing, user-read-playback-state"
	sp = spotipy.Spotify(
		client_credentials_manager=SpotifyOAuth(
			client_id=conf['spotify']['client_id'], 
			client_secret=conf['spotify']['client_secret'], 
			redirect_uri=conf['spotify']['redirect_uri'], 
			scope=scope))
	spotipy_res = sp.current_playback(additional_types='episode') # also get podcast info

	if spotipy_res is None:
		logging.warning('warning: currently no song is playing. skipping.')
		return None
		
	elif spotipy_res['currently_playing_type'] == 'track' or spotipy_res['currently_playing_type'] == 'episode':
		playing_type = spotipy_res['currently_playing_type']
		next_update = (spotipy_res["item"]["duration_ms"] / 1000) - (spotipy_res["progress_ms"] / 1000)
		if playing_type == 'track':
			(title, subtitle, album_art) = _extract_track(spotipy_res)
		else:
			(title, subtitle, album_art) = _extract_episode(spotipy_res)
		
		return (title, subtitle, album_art, playing_type, next_update)

	else: 
		logging.error('unknown playback type')
		return None


def _extract_track(spotipy_res):
	track_name = spotipy_res['item']['name']
	artists = spotipy_res['item']['artists']
	imgs = spotipy_res['item']['album']['images']

	names = []
	for artist in artists:
		names.append(artist['name'])
	artistnames = ", ".join(names)
	
	return (track_name, artistnames, _extract_sized_album_art(imgs))


def _extract_episode(spotipy_res):
	episode_name = spotipy_res['item']['name']
	show_name = spotipy_res['item']['show']['name']
	imgs = spotipy_res['item']['images']

	return (episode_name, show_name, _extract_sized_album_art(imgs))


def _extract_sized_album_art(res_imgs):
	img = None
	for i in res_imgs:
		if 'width' in i and i['width'] == bpm_render.IMAGE_WIDTH:
			img = i
	return img
