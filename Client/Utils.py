from osmnx.projection import project_gdf
from numpy import cos, rad2deg, deg2rad

class Utils:
    @staticmethod
    def filter_features_by_area(features, area):
        features = features[features.geometry.type.isin(["Polygon", "MultiPolygon"])]
        features = project_gdf(features)
        features["area"] = features["geometry"].area
        features = features[features["area"] > area]
        features = project_gdf(features, to_latlong = True)
        return features
    
    @staticmethod
    def add_meters_to_point_lon(point, dist):
        point[0] = point[0] + rad2deg(dist / 6378000)
        return point
    
    @staticmethod
    def add_meters_to_point_lat(point, dist):
        point[1] = point[1] + rad2deg(dist / 6378000) / cos(deg2rad(point[0]))
        return point