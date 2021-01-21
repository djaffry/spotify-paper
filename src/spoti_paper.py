
import time
import _thread
import logging

from . import api_spotify
from . import bpm_render

prev_title = ""
prev_subtitle = ""
prev_image = ""

epd_lock = _thread.allocate_lock()
thread_counter = 0

def cycle(epd=None):
    while True:
        current_playback = api_spotify.get_currently_playing()
        if current_playback is None:
            logging.info('no current_playback, sleeping')
            time.sleep(60 * 10)
            continue

        (image, updated) = _get_latest_image(current_playback)
        if updated:
            _display_image(image=image, epd=epd)
        (_, _, _, _, next_update) = current_playback

        while True: # check if playback has been skipped, if yes, update image
            time.sleep(5)
            current_playback = api_spotify.get_currently_playing()
            (image, updated) = _get_latest_image(current_playback)
            if updated:
                logging.info('playback skipped')
                _display_image(image=image, epd=epd)
                (_, _, _, _, next_update) = current_playback        
            else:
                break

        logging.debug('playback, sleeping for {} seconds'.format(next_update))
        time.sleep(next_update - api_spotify.API_LATENCY_SECS)


def _is_same_title_as_last_udpate(title, subtitle):
    global prev_title, prev_subtitle
    if prev_title != title or prev_subtitle != subtitle:
        return False
    return True


def _get_latest_image(current_playback=None):
    global prev_title, prev_subtitle, prev_image
    if current_playback is None:
        logging.debug('no current_playback, keep old image')
        image = prev_image
        updated = False

    else:
        (title, subtitle, album_art, playing_type, next_update) = current_playback    
        if _is_same_title_as_last_udpate(title, subtitle):
            logging.debug('same title & subtitle. no image refresh')
            image = prev_image
            updated = False
        else:
            image = bpm_render.draw_image(title, subtitle, album_art)
            prev_image = image
            prev_title = title
            prev_subtitle = subtitle
            updated = True
            logging.debug('title: {} / subtitle: {} / playing type: {} \n album art: {} / next update: {}' \
                .format(title, subtitle, playing_type, album_art != {}, next_update))
    return (image, updated)


def _display_image(image, epd=None):
    if epd is None:
        image.show()
    else:
        global thread_counter
        thread_counter = thread_counter + 1
        _thread.start_new_thread(_epd_display, (image, epd, epd_lock, thread_counter))


def _epd_display(image, epd, epd_lock, t_id):
    with epd_lock: # only one thread update epd at once
        global thread_counter
        logging.debug('global thread_counter: {} t_id: {} / thread_counter == t_id: ' \
            .format(thread_counter, t_id, thread_counter == t_id))
        if (thread_counter == t_id): # only allow latest thread to update epd
            epd.display_4Gray(epd.getbuffer_4Gray(image))
