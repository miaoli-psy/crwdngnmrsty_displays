from math import atan2, degrees
from shapely.geometry import Point
from shapely.affinity import scale, rotate


class Ellipse:
    def __init__(self, ellipse_center_coordinate, ka, kb):
        self.ellipse_center_coordinate = ellipse_center_coordinate
        self.ka = ka
        self.kb = kb

    def get_radial_angle(self):
        return degrees(atan2(self.ellipse_center_coordinate[1], self.ellipse_center_coordinate[0]))

    def get_polygon(self):
        p = Point(self.ellipse_center_coordinate)
        c = p.buffer(1)
        ellipse_polygon = scale(c, self.ka, self.kb)
        ellipse_polygon = rotate(geom = ellipse_polygon,
                                 angle = self.get_radial_angle(),
                                 origin = "centroid")
        return ellipse_polygon


if __name__ == '__main__':
    debug = True
    if debug:
        e = Ellipse((1.732, 1), 2, 0.5)
        e.get_polygon()