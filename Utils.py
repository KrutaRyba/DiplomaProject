from osmnx.projection import project_gdf

class Utils:
    @staticmethod
    def filter_features_by_area(features, area):
        features = features[features.geometry.type.isin(["Polygon", "MultiPolygon"])]
        features = project_gdf(features)
        features["area"] = features["geometry"].area
        features = features[features["area"] > area]
        features = project_gdf(features, to_latlong = True)
        return features