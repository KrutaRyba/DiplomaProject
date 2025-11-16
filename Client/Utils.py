from math import cos, radians, degrees, exp2

class Utils:
    @staticmethod
    def add_meters_to_point_lon(point, dist):
        point[0] = point[0] + degrees(dist / 6378000)
        return point
    
    @staticmethod
    def add_meters_to_point_lat(point, dist):
        point[1] = point[1] + degrees(dist / 6378000) / cos(radians(point[0]))
        return point
    
    @staticmethod
    def horizontal_distance(latitude, zoom_level):
        return (40075016.686 * cos(radians(latitude))) / exp2(zoom_level)