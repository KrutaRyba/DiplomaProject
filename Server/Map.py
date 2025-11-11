from osmnx import utils_geo
from Utils import Utils

class Map:
    def __init__(self, center, zoom):
        self.__center = center
        self.__zoom = zoom
        self.dist = None
        self.bbox = None
        self.bbox_data = None
        self.features = None
        self.network = None
        self.administrative_levels = None
        self.street_widths = None
        self.railway_width = None
        self.refresh()

    def refresh(self):
        self.dist = Utils.horizontal_distance(self.center[0], self.zoom)
        self.bbox = utils_geo.bbox_from_point(self.center, self.dist)
        self.bbox_data = utils_geo.bbox_from_point(self.center, Utils.horizontal_distance(self.center[0], max(self.zoom - 2, 4)))

    @property
    def zoom(self):
        return self.__zoom
    @zoom.setter
    def zoom(self, value):
        self.__zoom = value
        self.refresh()
    @zoom.deleter
    def zoom(self):
        del self.__zoom

    @property
    def center(self):
        return self.__center
    @center.setter
    def center(self, value):
        self.__center = value
        self.refresh()
    @center.deleter
    def center(self):
        del self.__center