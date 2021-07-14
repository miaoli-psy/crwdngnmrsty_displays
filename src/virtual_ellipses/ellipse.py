from math import atan2, degrees
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.affinity import scale, rotate
from descartes import PolygonPatch
from enum import Enum
from shapely.ops import unary_union


class Orientation(Enum):
    Radial = 1
    Tangential = 2
    Both = 3


class Ellipse:
    def __init__(self, ellipse_center_coordinate, ka, kb, orientation):
        self.ellipse_center_coordinate = ellipse_center_coordinate
        self.orientation = orientation
        if ka < kb:
            print(f"Warning: Expected ka > kb, but input ka = {ka}, kb = {kb}")
            self.ka = kb
            self.kb = ka
        else:
            self.ka = ka
            self.kb = kb
        # radial angle是径向椭圆中心与原点连线与横轴夹角
        self.angle = degrees(atan2(ellipse_center_coordinate[1], ellipse_center_coordinate[0]))
        self.polygon = self.get_polygon()

    def get_polygon(self):
        # center to Point center
        p = Point(self.ellipse_center_coordinate)
        c = p.buffer(1)
        # get original ellipse
        polygon_horizontal = scale(c, self.ka, self.kb)
        # 这里的旋转是把水平椭圆（0度）以椭圆中心逆时针选着（正度数）
        ellipse_polygon_radial = rotate(geom = polygon_horizontal,
                                        angle = self.angle,
                                        origin = "centroid")

        ellipse_polygon_tangential = rotate(geom = polygon_horizontal,
                                            angle = self.angle + 90,
                                            origin = "centroid")

        if self.orientation == Orientation.Radial:
            return ellipse_polygon_radial
        elif self.orientation == Orientation.Tangential:
            return ellipse_polygon_tangential
        elif self.orientation == Orientation.Both:
            return unary_union([ellipse_polygon_radial, ellipse_polygon_tangential])

    def plot_ellipse_polygon(self, axes_lim = None):
        if axes_lim is None:
            axes_lim = [-20, 20]
        patch = PolygonPatch(self.get_polygon())
        ax = plt.subplot()
        ax.add_artist(patch)
        ax.set_xlim(axes_lim)
        ax.set_ylim(axes_lim)
        ax.set_aspect('equal', 'box')
        plt.show()

    # def get_intersects(self, other_polygon):
    #
    #     return self.get_polygon_radial().intersection(other_polygon.get_polygon_radial())


if __name__ == '__main__':
    debug = False
    if debug:
        e = Ellipse((10, 17.32), 2, 5)
        e.get_radial_angle()
        e.plot_ellipse_polygon(angle = "tangential")