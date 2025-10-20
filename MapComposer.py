from APIConnector import APIConnector

class Features:
    def __init__(self):
        self.buildings = None
        self.grass = None
        self.sand = None
        self.water = None

class Network:
    def __init__(self):
        self.highway = None
        self.railway = None

class MapComposer:
    def __init__(self):
        self.API = APIConnector()

    def compose(self, map):
        if (map.zoom == 1):
            map.features, map.network, map.street_widths = self.__zoom_level_1__(map.bbox)
            map.railway_width = 1
        elif (map.zoom == 2):
            pass
        elif (map.zoom == 3):
            pass
    
    def __zoom_level_1__(self, bbox):
        features = Features()
        network = Network()
        features.buildings = self.API.get_features(bbox, {"building": True})
        features.grass = self.API.get_features(bbox, {"landuse": ["allotments", "flowerbed", "forest", "meadow", "orchard", "plant_nursery", "vineyard", "cemetery", "grass", "recreation_ground", "village_green"],
                                                           "leisure": ["garden", "park", "pitch"],
                                                           "natural": ["grassland", "heath", "scrub", "tree", "tree_row", "wood"]})
        features.sand = self.API.get_features(bbox, {"natural": ["beach", "shoal", "sand"]})
        features.water = self.API.get_features(bbox, {"landuse": ["basin"],
                                                           "leisure": ["swimming_pool"],
                                                           "natural": ["bay", "reef", "spring", "strait", "water"]})
        network.highway = self.API.get_network(bbox, "all", None)
        network.railway = self.API.get_network(bbox, None, "['railway'~'construction|disused|funicular|light_rail|miniature|monorail|narrow_gauge|rail|subway|tram']")
        street_widths = {"motorway": 8,
                              "trunk": 7, "primary": 7, "secondary": 7, "tertiary": 7,
                              "unclassified": 5, "residential": 5, "motorway_link": 5, "trunk_link": 5, "primary_link": 5, "secondary_link": 5, "tertiary_link": 5, "living_street": 5, "pedestrian": 5,
                              "service": 3, "raceway": 3, "road": 3}
        return (features, network, street_widths)