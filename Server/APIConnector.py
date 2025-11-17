from networkx import MultiDiGraph
from osmnx import features, graph, _errors
from pandas import DataFrame

class APIConnector:
    def get_features(self, bbox, tags):
        feature = DataFrame()
        try:
            feature = features.features_from_bbox(bbox, tags)
        except (_errors.InsufficientResponseError):
            print("  Not found")
        return feature
    
    def get_network(self, bbox, network_type, custom_filter):
        network = MultiDiGraph()
        try:
            network = graph.graph_from_bbox(bbox, network_type = network_type, custom_filter = custom_filter, truncate_by_edge = True, retain_all = True)
        except (ValueError):
            print("  Not found")
        return network