from typing import Any
from geopandas import GeoDataFrame
from networkx import MultiDiGraph

class Features:
    def __init__(self) -> None:
        self.buildings: GeoDataFrame
        self.grass: GeoDataFrame
        self.sand: GeoDataFrame
        self.water: GeoDataFrame
        self.amenities:GeoDataFrame

class Network:
    def __init__(self) -> None:
        self.highway: MultiDiGraph
        self.railway: MultiDiGraph

class Street:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.sub_streets: list[dict[str, Any]] = []