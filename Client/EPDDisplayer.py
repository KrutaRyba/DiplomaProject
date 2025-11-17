from EPDDisplay import EPDDisplay
from PIL import Image

class EPDDisplayer:
    def __init__(self, EPD: EPDDisplay) -> None:
        self.EPD: EPDDisplay = EPD

    def init_epd(self) -> None:
        print("----- Start EPD init -----")
        self.EPD.init()
        print("----- EPD init done -----")

    def sleep(self) -> None:
        self.EPD.sleep()

    def display(self) -> None:
        Himage = Image.open("Map.png")
        resized_img = Himage.resize((self.EPD.width, self.EPD.width))
        left = (self.EPD.width - self.EPD.width) / 2
        top = (self.EPD.width - self.EPD.height) / 2
        right = (self.EPD.width + self.EPD.width) / 2
        bottom = (self.EPD.width + self.EPD.height) / 2
        resized_img = resized_img.crop((left, top, right, bottom))
        resized_img.save("Map.bmp")
        img = Image.open("Map.bmp")
        self.EPD.display_image(img)
        img.close()

    def exit(self) -> None:
        self.EPD.exit()