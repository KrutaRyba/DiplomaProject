from osmnx import features, graph, _errors
from geopandas import GeoDataFrame
from networkx import MultiDiGraph
from APIConnector import APIConnector

class OSMNXConnector(APIConnector):
    def get_features(self, bbox: tuple[float, float, float, float], tags: dict[str, bool | str | list[str]]) -> GeoDataFrame:
        feature = GeoDataFrame()
        try:
            feature = features.features_from_bbox(bbox, tags)
        except (_errors.InsufficientResponseError):
            print("  Not found")
        return feature
    
    def get_network(self, bbox: tuple[float, float, float, float], network_type: str | None, custom_filter: str | None) -> MultiDiGraph:
        network = MultiDiGraph()
        type = "all" if (network_type == None) else network_type
        try:
            network = graph.graph_from_bbox(bbox, network_type = type, custom_filter = custom_filter, truncate_by_edge = True, retain_all = True)
        except (ValueError):
            print("  Not found")
        return network