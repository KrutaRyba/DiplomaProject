from abc import ABC, abstractmethod
from typing import Any

class EPDDisplay(ABC):
    @abstractmethod
    def init(self) -> None:
        self.width: int
        self.height: int
    @abstractmethod
    def sleep(self) -> None:
        pass
    @abstractmethod
    def display_image(self, img: Any) -> None:
        pass
    @abstractmethod
    def exit(self) -> None:
        pass

class PhysicalEPD(EPDDisplay):
    def init(self) -> None:
        from waveshare_epd import epd7in3f
        self.EPD = epd7in3f.EPD()
        self.EPD.init()
        self.EPD.Clear()
        self.width: int = self.EPD.width
        self.height: int = self.EPD.height
    
    def sleep(self) -> None:
        self.EPD.sleep()

    def display_image(self, img: Any) -> None:
        self.EPD.display(self.EPD.getbuffer(img))

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

    def display_image(self, img: Any) -> None:
        print("<<Emulated EPD display_image>>")
        img.show()

    def exit(self) -> None:
        print("<<Emulated EPD exit>>")