
import sys
import os
import time
import traceback
import logging

from driver import epd4in2
from src import spoti_paper



try:
    logging.info("Print generated image to EPD")

    epd = epd4in2.EPD()
    logging.info("EPD Init and Cleared")
    epd.init()
    epd.Clear()

    spoti_paper.cycle(epd=epd)
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("CTRL + C :")
    epd4in2.epdconfig.module_exit()
    exit()
