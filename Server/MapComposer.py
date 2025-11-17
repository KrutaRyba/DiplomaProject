from APIConnector import APIConnector
from LocalConnector import LocalConnector
from networkx import MultiDiGraph
from pandas import DataFrame
from Utils import Utils

class Features:
    def __init__(self):
        self.buildings = None
        self.grass = None
        self.sand = None
        self.water = None
        self.amenities = None

class Network:
    def __init__(self):
        self.highway = None
        self.railway = None

class MapComposer:
    def __init__(self):
        self.API = LocalConnector()

    def compose(self, map):
        if (map.zoom == 19 or map.zoom == 18):
            map.features, map.network, map.administrative_levels = self.__zoom_level_close(map.bbox_data, map.dist)
            map.street_widths = {"motorway": 8,
                                 "trunk": 7, "primary": 7, "secondary": 7, "tertiary": 7,
                                 "unclassified": 5, "residential": 5, "motorway_link": 5, "trunk_link": 5, "primary_link": 5, "secondary_link": 5, "tertiary_link": 5, "living_street": 5, "pedestrian": 5,
                                 "service": 3, "raceway": 3, "road": 3}
            map.railway_width = 2
        elif (map.zoom == 17 or map.zoom == 16):
            map.features, map.network, map.administrative_levels = self.__zoom_level_close(map.bbox_data, map.dist)
            map.street_widths = {"motorway": 6,
                                 "trunk": 5, "primary": 5, "secondary": 5, "tertiary": 5,
                                 "unclassified": 3, "residential": 3, "motorway_link": 3, "trunk_link": 3, "primary_link": 3, "secondary_link": 3, "tertiary_link": 3, "living_street": 3, "pedestrian": 3}
            map.railway_width = 2
        elif (map.zoom == 15 or map.zoom == 14):
            map.features, map.network, map.administrative_levels = self.__zoom_level_medium_close(map.bbox_data, map.dist)
            map.street_widths = {"motorway": 4,
                                 "trunk": 3, "primary": 3, "secondary": 3, "tertiary": 3}
            map.railway_width = 1
        elif (map.zoom == 13 or map.zoom == 12):
            map.features, map.network, map.administrative_levels = self.__zoom_level_medium(map.bbox_data, map.dist)
            map.street_widths = {"motorway": 3,
                                 "trunk": 2, "primary": 2, "secondary": 2, "tertiary": 2}
            map.railway_width = 1
        elif (map.zoom == 11 or map.zoom == 10):
            map.features, map.network, map.administrative_levels = self.__zoom_level_medium_far(map.bbox_data, map.dist)
            map.street_widths = {"motorway": 2}
            map.railway_width = 0.5
        elif (map.zoom == 9 or map.zoom == 8):
            map.features, map.network, map.administrative_levels = self.__zoom_level_far(map.bbox_data, map.dist)
            map.street_widths = {"motorway": 2}
            map.railway_width = 0.5
        elif (map.zoom == 7 or map.zoom == 6):
            map.features, map.network, map.administrative_levels = self.__zoom_level_super_far(map.bbox_data, map.dist)
            map.street_widths = {"motorway": 1}
            map.railway_width = 0
    
    def __zoom_level_close(self, bbox, _):
        features = Features()
        network = Network()
        print("----- Start download -----")
        print("> Buildings")
        features.buildings = self.API.get_features(bbox, {"building": True})
        print("> Amenities")
        features.amenities = self.API.get_features(bbox, {"amenity": True})
        print("> Grass")
        features.grass = self.API.get_features(bbox, {"landuse": ["allotments", "farmland", "flowerbed", "forest", "meadow", "orchard", "plant_nursery", "vineyard", "cemetery", "grass", "recreation_ground", "village_green"],
                                                      "leisure": ["garden", "park", "pitch"],
                                                      "natural": ["grassland", "heath", "scrub", "tree", "tree_row", "wood"]})
        print("> Sand")
        features.sand = self.API.get_features(bbox, {"natural": ["beach", "shoal", "sand"]})
        print("> Water")
        features.water = self.API.get_features(bbox, {"landuse": ["basin"],
                                                      "leisure": ["swimming_pool"],
                                                      "natural": ["bay", "reef", "spring", "strait", "water"]})
        print("> Highway")
        network.highway = self.API.get_network(bbox, "all", None)
        print("> Railway")
        network.railway = self.API.get_network(bbox, None, "['railway'~'construction|disused|funicular|light_rail|miniature|monorail|narrow_gauge|rail|subway|tram']")
        print("> Administrative levels")
        admin_levels = self.API.get_features(bbox, {"place": ["state", "country"]})
        print("----- Download done -----")
        #amen = self.API.get_features(bbox, {"amenity": True})
        return (features, network, admin_levels)
    
    def __zoom_level_medium_close(self, bbox, _):
        features = Features()
        network = Network()
        print("----- Start download -----")
        print("> Buildings")
        features.buildings = self.API.get_features(bbox, {"building": True})
        print("> Amenities")
        features.amenities = DataFrame()
        print("  Skipped")
        print("> Grass")
        features.grass = self.API.get_features(bbox, {"landuse": ["allotments", "farmland", "forest", "meadow", "orchard", "plant_nursery", "grass", "recreation_ground"],
                                                      "leisure": ["park", "pitch"],
                                                      "natural": ["grassland", "heath", "scrub", "wood"]})
        print("> Sand")
        features.sand = self.API.get_features(bbox, {"natural": ["beach", "shoal", "sand"]})
        print("> Water")
        features.water = self.API.get_features(bbox, {"natural": ["bay", "reef", "strait", "water"]})
        print("> Highway")
        network.highway = self.API.get_network(bbox, "drive", None)
        print("> Railway")
        network.railway = self.API.get_network(bbox, None, "['railway'~'light_rail|monorail|narrow_gauge|rail|subway|tram']")
        print("> Administrative levels")
        admin_levels = self.API.get_features(bbox, {"place": ["suburb", "village", "town", "city", "state", "country"]})
        print("----- Download done -----")
        return (features, network, admin_levels)
    
    def __zoom_level_medium(self, bbox, dist):
        features = Features()
        network = Network()
        print("----- Start download -----")
        print("> Buildings")
        features.buildings = DataFrame()
        print("  Skipped")
        print("> Amenities")
        features.amenities = DataFrame()
        print("  Skipped")
        print("> Grass")
        grass = self.API.get_features(bbox, {"landuse": ["allotments", "farmland", "forest", "meadow", "grass"],
                                             "leisure": ["park"],
                                             "natural": ["grassland", "heath", "scrub", "wood"]})
        features.grass = Utils.filter_features_by_area(grass, dist)
        print("> Sand")
        features.sand = DataFrame()
        print("  Skipped")
        print("> Water")
        water = self.API.get_features(bbox, {"natural": ["bay", "reef", "strait", "water"]})
        features.water = Utils.filter_features_by_area(water, dist)
        print("> Highway")
        network.highway = self.API.get_network(bbox, None, "['highway'~'motorway|trunk|primary|secondary|tertiary|residential']")
        print("> Railway")
        network.railway = self.API.get_network(bbox, None, "['railway'~'light_rail|narrow_gauge|rail']")
        print("> Administrative levels")
        admin_levels = self.API.get_features(bbox, {"place": ["suburb", "village", "town", "city", "state", "country"]})
        print("----- Download done -----")
        return (features, network, admin_levels)
    
    def __zoom_level_medium_far(self, bbox, dist):
        features = Features()
        network = Network()
        print("----- Start download -----")
        print("> Buildings")
        features.buildings = DataFrame()
        print("  Skipped")
        print("> Amenities")
        features.amenities = DataFrame()
        print("  Skipped")
        print("> Grass")
        grass = self.API.get_features(bbox, {"landuse": ["allotments", "farmland", "forest", "meadow", "grass"],
                                             "natural": ["grassland", "heath", "scrub", "wood"]})
        features.grass = Utils.filter_features_by_area(grass, dist)
        print("> Sand")
        features.sand = DataFrame()
        print("  Skipped")
        print("> Water")
        water = self.API.get_features(bbox, {"natural": ["bay", "reef", "strait", "water"]})
        features.water = Utils.filter_features_by_area(water, dist)
        print("> Highway")
        network.highway = self.API.get_network(bbox, None, "['highway'~'motorway|trunk|primary|secondary|tertiary']")
        print("> Railway")
        network.railway = self.API.get_network(bbox, None, "['railway'~'rail']")
        print("> Administrative levels")
        admin_levels = self.API.get_features(bbox, {"place": ["town", "city", "state", "country"]})
        print("----- Download done -----")
        return (features, network, admin_levels)
    
    def __zoom_level_far(self, bbox, dist):
        features = Features()
        network = Network()
        print("----- Start download -----")
        print("> Buildings")
        features.buildings = DataFrame()
        print("  Skipped")
        print("> Amenities")
        features.amenities = DataFrame()
        print("  Skipped")
        print("> Grass")
        grass = self.API.get_features(bbox, {"natural": ["grassland"]})
        features.grass = Utils.filter_features_by_area(grass, dist)
        print("> Sand")
        features.sand = DataFrame()
        print("  Skipped")
        print("> Water")
        water = self.API.get_features(bbox, {"natural": ["water"]})
        features.water = Utils.filter_features_by_area(water, dist)
        print("> Highway")
        network.highway = self.API.get_network(bbox, None, "['highway'~'motorway|trunk|primary']")
        print("> Railway")
        network.railway = self.API.get_network(bbox, None, "['railway'~'rail']")
        print("> Administrative levels")
        admin_levels = self.API.get_features(bbox, {"place": ["town", "city", "state", "country"]})
        print("----- Download done -----")
        return (features, network, admin_levels)
    
    def __zoom_level_super_far(self, bbox, dist):
        features = Features()
        network = Network()
        print("----- Start download -----")
        print("> Buildings")
        features.buildings = DataFrame()
        print("  Skipped")
        print("> Amenities")
        features.amenities = DataFrame()
        print("  Skipped")
        print("> Grass")
        features.grass = DataFrame()
        print("  Skipped")
        print("> Sand")
        features.sand = DataFrame()
        print("  Skipped")
        print("> Water")
        features.water = DataFrame()
        print("  Skipped")
        print("> Highway")
        network.highway = MultiDiGraph()
        print("  Skipped")
        print("> Railway")
        network.railway = MultiDiGraph()
        print("  Skipped")
        print("> Administrative levels")
        admin_levels = self.API.get_features(bbox, {"place": ["state", "country"]})
        print("----- Download done -----")
        return (features, network, admin_levels)