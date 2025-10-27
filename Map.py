from osmnx import utils_geo
import numpy

class Map:
    def __init__(self, center, zoom):
        self._center = center
        self._zoom = zoom
        self.dist = None
        self.bbox = None
        self.features = None
        self.network = None
        self.street_widths = None
        self.railway_width = None
        self.__refresh__()

    def __refresh__(self):
        self.dist = (40075016.686 * numpy.cos(numpy.radians(self.center[0]))) / numpy.exp2(self.zoom)
        self.bbox = utils_geo.bbox_from_point(self.center, self.dist)

    @property
    def zoom(self):
        return self._zoom
    @zoom.setter
    def zoom(self, value):
        self._zoom = value
        self.__refresh__()
    @zoom.deleter
    def zoom(self):
        del self._zoom

    @property
    def center(self):
        return self._center
    @center.setter
    def center(self, value):
        self._center = value
        self.__refresh__()
    @center.deleter
    def center(self):
        del self._center