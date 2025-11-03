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
        print("----- Start EPD init -----")
        self.EPD.init()
        self.EPD.Clear()
        print("----- EPD init done -----")

    def sleep(self):
        self.EPD.sleep()

    def display(self):
        Himage = Image.open("Map.png")
        resized_img = Himage.resize((self.EPD.width, self.EPD.width))
        left = (self.EPD.width - self.EPD.width) / 2
        top = (self.EPD.width - self.EPD.height) / 2
        right = (self.EPD.width + self.EPD.width) / 2
        bottom = (self.EPD.width + self.EPD.height) / 2
        resized_img = resized_img.crop((left, top, right, bottom))
        resized_img.save("Map.bmp")
        img = Image.open("Map.bmp")
        self.EPD.display(self.EPD.getbuffer(img))
        img.close()