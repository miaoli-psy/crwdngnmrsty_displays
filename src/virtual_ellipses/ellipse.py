from math import atan2, degrees


class Ellipse:
    def __init__(self, ellipse_center_coordinate, ka, kb):
        self.ellipse_center_coordinate = ellipse_center_coordinate
        self.ka = ka
        self.kb = kb

    def get_radial_angle(self):
        return degrees(atan2(self.ellipse_center_coordinate[1], self.ellipse_center_coordinate[0]))


if __name__ == '__main__':
    debug = True
    if debug:
        e = Ellipse((1.732, 1), 3, 5)
