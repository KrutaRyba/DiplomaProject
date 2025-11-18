from abc import ABC, abstractmethod
from PIL.Image import Image, open

class EPDDisplay(ABC):
    @abstractmethod
    def init(self) -> None:
        self.width: int
        self.height: int
    @abstractmethod
    def sleep(self) -> None:
        pass
    @abstractmethod
    def display_image(self) -> None:
        pass
    @abstractmethod
    def exit(self) -> None:
        pass

    def __get_image(self) -> Image:
        Himage = open("Map.png")
        resized_img = Himage.resize((self.width, self.width))
        left = (self.width - self.width) / 2
        top = (self.width - self.height) / 2
        right = (self.width + self.width) / 2
        bottom = (self.width + self.height) / 2
        resized_img = resized_img.crop((left, top, right, bottom))
        resized_img.save("Map.bmp")
        return open("Map.bmp")


class PhysicalEPD(EPDDisplay):
    def init(self) -> None:
        from waveshare_epd import epd7in3f
        print("----- Start EPD init -----")
        self.EPD = epd7in3f.EPD()
        self.EPD.init()
        self.EPD.Clear()
        print("----- EPD init done -----")
        self.width: int = self.EPD.width
        self.height: int = self.EPD.height
    
    def sleep(self) -> None:
        self.EPD.sleep()

    def display_image(self) -> None:
        img = super().__get_image()
        self.EPD.display(self.EPD.getbuffer(img))
        img.close()

    def exit(self) -> None:
        from waveshare_epd import epd7in3f
        epd7in3f.epdconfig.module_exit(cleanup=True)


class EmulatedEPD(EPDDisplay):
    def init(self) -> None:
        print("<<Emulated EPD init>>")
        self.width: int = 800
        self.height: int = 480
    
    def sleep(self) -> None:
        print("<<Emulated EPD sleep>>")

    def display_image(self) -> None:
        print("<<Emulated EPD display_image>>")
        img = super().__get_image()
        img.show()
        img.close()

    def exit(self) -> None:
        print("<<Emulated EPD exit>>")