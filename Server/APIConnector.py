from geopandas import GeoDataFrame
from networkx import MultiDiGraph
from abc import ABC, abstractmethod

class APIConnector(ABC):
    @abstractmethod
    def get_features(self, bbox: tuple[float, float, float, float], tags: dict[str, bool | str | list[str]]) -> GeoDataFrame:
        pass
    @abstractmethod
    def get_network(self, bbox: tuple[float, float, float, float], network_type: str | None, custom_filter: str | None) -> MultiDiGraph:
        pass