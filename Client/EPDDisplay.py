from abc import ABC, abstractmethod

class EPDDisplay(ABC):
    @abstractmethod
    def init(self):
        pass
    @abstractmethod
    def sleep(self):
        pass
    @abstractmethod
    def display_image(self, buffer):
        pass

class PhysicalEPD(EPDDisplay):
    def init(self):
        import sys
        import os
        libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
        if os.path.exists(libdir):
            sys.path.append(libdir)
        from waveshare_epd import epd7in3f

        self.EPD = epd7in3f.EPD()
        self.EPD.init()
        self.EPD.Clear()
        self.width = self.EPD.width
        self.height = self.EPD.height
    
    def sleep(self):
        self.EPD.sleep()

    def display_image(self, img):
        self.EPD.display(self.EPD.getbuffer(img))

class EmulatedEPD(EPDDisplay):
    def init(self):
        print("<<Emulated EPD init>>")
        self.width = 800
        self.height = 480
    
    def sleep(self):
        print("<<Emulated EPD sleep>>")

    def display_image(self, img):
        print("<<Emulated EPD display_image>>")
        img.show()