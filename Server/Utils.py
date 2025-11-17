from numpy import cos, radians, exp2
from os.path import dirname, join
from osmnx.projection import project_gdf
import sys

class Utils:
    @staticmethod
    def filter_features_by_area(features, area):
        features = features[features.geometry.type.isin(["Polygon", "MultiPolygon"])]
        features = project_gdf(features)
        features["area"] = features["geometry"].area
        features = features[features["area"] > area]
        if (features.empty): return features
        features = project_gdf(features, to_latlong = True)
        return features
    
    @staticmethod
    def horizontal_distance(latitude, zoom_level):
        return (40075016.686 * cos(radians(latitude))) / exp2(zoom_level)
    
    @staticmethod
    def find_file(file, folder = None):
        if getattr(sys, "frozen", False): datadir = dirname(sys.executable)
        else: datadir = dirname(__file__)
        return join(datadir, file) if (folder == None) else join(datadir, folder, file)
    
class Definitions:
    OSM_FOLDER = ".osm_tmp"
    MAP_FOLDER = "img"