import random
import matplotlib.pyplot as plt
from shapely.geometry import Point
from descartes import PolygonPatch


def get_random_point_in_polygon(poly):
    minx, miny, maxx, maxy = poly.bounds
    while True:
        point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if poly.contains(point):
            return point


def plot_polygon(polygonlist, axes_lim = None):
    if axes_lim is None:
        axes_lim = [-20, 20]
    ax = plt.subplot()
    for poly in polygonlist:
        patch = PolygonPatch(poly)
        ax.add_artist(patch)
    ax.set_xlim(axes_lim)
    ax.set_ylim(axes_lim)
    ax.set_aspect('equal', 'box')
    plt.show()


def get_intersect_poly(poly1, poly2):
    return poly1.intersection(poly2)


def polypoint_to_coords(point):
    return list(point.coords)[0]