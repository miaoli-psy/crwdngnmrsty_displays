from math import atan2, degrees
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.affinity import scale, rotate
from descartes import PolygonPatch


class Ellipse:
    def __init__(self, ellipse_center_coordinate, ka, kb):
        self.ellipse_center_coordinate = ellipse_center_coordinate
        self.ka = ka
        self.kb = kb

    def get_radial_angle(self):
        # radial angle是椭圆中心与原点连线与横轴夹角
        return degrees(atan2(self.ellipse_center_coordinate[1], self.ellipse_center_coordinate[0]))

    def get_polygon(self):
        p = Point(self.ellipse_center_coordinate)
        c = p.buffer(1)
        ellipse_polygon = scale(c, self.ka, self.kb)
        # 这里的旋转是把竖直椭圆（0度）以椭圆中心逆时针选着（正度数）
        # 与radial angele相差90度
        ellipse_polygon = rotate(geom = ellipse_polygon,
                                 angle = self.get_radial_angle() + 90,
                                 origin = "centroid")
        return ellipse_polygon

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


if __name__ == '__main__':
    debug = True
    if debug:
        e = Ellipse((-1.732, 1), 2, 0.5)
        e.get_polygon()
        e.plot_ellipse_polygon()
