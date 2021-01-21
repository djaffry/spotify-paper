# Spoti Paper :tv::radio::notes:

If you are like me and have some Wi-Fi Speaker without displays and listen to auto-generated playlists, 
you might sometimes wonder what song is currently playing. Or you might wonder what the album cover looks like (in black and white).

**Spoti Paper** displays the album cover, song title and artist information from your currently playing songs on Spotify.

<p align="center">
  <img height=500 src="https://github.com/djaffry/spoti-paper/blob/master/pics/never.jpg" alt="Spoti Paper in action">
</p>

## Hardware 
- 400x300, 4.2inch E-Ink display module for Raspberry Pi &rarr; [waveshare Wiki](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module)
- Raspberry Pi Zero W with soldered headers or any Raspberry Pi 2 and up (tested with zero W and PI 3B+) &rarr; [Raspberry Pi Website](https://www.raspberrypi.org/products/)

## Getting Started


### Spotify Dashboard

* Log in to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login) and create a new app.
* Click on :gear: EDIT SETTINGS
  * Add `http://127.0.0.1:8080/callback/` as redirect URI
* To generate a Spotify Cache for your Pi, you need a PC, a monitor and a Web Browser. You can do this on any PC and transfer the cache afterwards to your Pi
  * Clone this project: `git clone https://github.com/djaffry/spoti-paper.git`
  * Install needed libraries for cache generation: `pip3 install -r requirements_token.txt`
  * Rename `config-skeleton.json` to `config.json` and insert your credentials from the dashboard
  * Run `python3 generate_cache.py`
  * This will generate a file called `.cache`. Copy this file to your Pi

### Raspberry Pi
 
* Clone this project: `git clone https://github.com/djaffry/spoti-paper.git`
* Install libraries: `pip3 install -r requirements.txt`
* Move the generated cache file to the root of this project
* Run `sudo nohup python3 epaper_run.py &` to display live Spotify information on your E-Paper 
  * Alternatively you can use `monitor_run.py` to display the album art as bitmap on your monitor
* Sit back and listen to music

