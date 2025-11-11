from numpy import cos, rad2deg, deg2rad

class Utils:
    @staticmethod
    def add_meters_to_point_lon(point, dist):
        point[0] = point[0] + rad2deg(dist / 6378000)
        return point
    
    @staticmethod
    def add_meters_to_point_lat(point, dist):
        point[1] = point[1] + rad2deg(dist / 6378000) / cos(deg2rad(point[0]))
        return point