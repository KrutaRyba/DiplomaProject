from math import cos, radians, degrees, exp2

class Utils:
    @staticmethod
    def add_meters_to_point_lat(point: list[float], dist: float) -> list[float]:
        p = [0.0, 0.0]
        p[0] = point[0] + degrees(dist / 6378000)
        p[1] = point[1]
        return p
    
    @staticmethod
    def add_meters_to_point_lon(point: list[float], dist: float) -> list[float]:
        p = [0.0, 0.0]
        p[1] = point[1] + degrees(dist / 6378000) / cos(radians(point[0]))
        p[0] = point[0]
        return p
    
    @staticmethod
    def horizontal_distance(latitude: float, zoom_level: int) -> float:
        return (40075016.686 * cos(radians(latitude))) / exp2(zoom_level)