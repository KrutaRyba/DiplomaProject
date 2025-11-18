from DataFrames import Features, Network
from geopandas import GeoDataFrame
from Utils import Utils
from osmnx import utils_geo

class Map:
    def __init__(self, center: tuple[float, float], zoom: int) -> None:
        self.__center: tuple[float, float] = center
        self.__zoom: int = zoom
        self.dist: float
        self.bbox: tuple[float, float, float, float]
        self.bbox_data: tuple[float, float, float, float]
        self.features: Features
        self.network: Network
        self.administrative_levels: GeoDataFrame
        self.street_widths: dict[str, float]
        self.railway_width: int | float
        self.__refresh()

    def __refresh(self) -> None:
        self.dist = Utils.horizontal_distance(self.center[0], self.zoom)
        self.bbox = utils_geo.bbox_from_point(self.center, self.dist)
        self.bbox_data = utils_geo.bbox_from_point(self.center, Utils.horizontal_distance(self.center[0], self.zoom - 2))

    @property
    def zoom(self) -> int:
        return self.__zoom
    @zoom.setter
    def zoom(self, value: int) -> None:
        self.__zoom = value
        self.__refresh()
    @zoom.deleter
    def zoom(self) -> None:
        del self.__zoom

    @property
    def center(self) -> tuple[float, float]:
        return self.__center
    @center.setter
    def center(self, value: tuple[float, float]) -> None:
        self.__center = value
        self.__refresh()
    @center.deleter
    def center(self) -> None:
        del self.__center