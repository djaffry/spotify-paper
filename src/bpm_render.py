
from PIL import Image, ImageDraw, ImageFont, ImageStat
from io import BytesIO
import requests
import logging

IMAGE_HEIGHT = 400
IMAGE_WIDTH = 300

def draw_image(title, subtitle, img):
	if img is not None:
		img_res = requests.get(img['url'])
		album_art = Image.open(BytesIO(img_res.content)).convert('L')
		album_art_color_median = ImageStat.Stat(album_art).median[0]
		album_art_dark = False if album_art_color_median > 127 else True
		
		logging.debug('image is {} / color median is: {}' \
			.format('dark' if album_art_dark else 'light',  album_art_color_median))
	
		image = Image.new('L', (IMAGE_WIDTH, IMAGE_HEIGHT), album_art_color_median) 
		font_color = 255 if album_art_dark else 0
		image.paste(album_art, (0, 0))

	else:
		logging.warning('current track/episode has no img')
		image = Image.new('L', (IMAGE_WIDTH, IMAGE_HEIGHT), 0) 
		font_color = 255

	title_font = ImageFont.truetype('fonts/Montserrat-Medium.ttf', 24)
	subtitle_font = ImageFont.truetype('fonts/Montserrat-Medium.ttf', 14)
	draw = ImageDraw.Draw(image)
	if title is not None:
		title = _fit_text(draw=draw, text=title, font=title_font, text_padding=16)
		draw.text((16, 325), title, font=title_font, fill=font_color)
	if subtitle is not None:
		subtitle = _fit_text(draw=draw, text=subtitle, font=subtitle_font, text_padding=16)
		draw.text((16, 355), subtitle, font=subtitle_font, fill=font_color)

	return image


def _fit_text(draw, text, font, text_padding):
	(_, _, end, _) = draw.textbbox((text_padding, 0), text, font=font)
	if end > IMAGE_WIDTH - text_padding:
		text = _fit_text(draw=draw, text=(text[:-2] + '…'), font=font, text_padding=text_padding)
	return text
