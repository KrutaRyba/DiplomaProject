import sys
import os
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image
from waveshare_epd import epd7in3f

class EPDDisplayer:
    def __init__(self):
        self.EPD = epd7in3f.EPD()

    def init_epd(self):
        self.EPD.init()
        self.EPD.Clear()

    def sleep(self):
        self.EPD.sleep()

    def display(self):
        Image.open("Map.png").save("Map.bmp")
        Himage = Image.open("Map.bmp")
        img = Himage.resize((self.EPD.width, self.EPD.height))
        self.EPD.display(self.EPD.getbuffer(img))