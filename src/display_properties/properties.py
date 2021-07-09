from scipy.spatial import distance, ConvexHull
from itertools import combinations
import numpy as np


def displayposi_to_array(posilist):
    return np.asarray(posilist)


def get_hull(posilist):
    return ConvexHull(displayposi_to_array(posilist))


def cal_average(lst):
    return round(sum(lst)/len(lst),2)


def get_all_eccentricity(posilist):
    posilist_array = displayposi_to_array(posilist)
    return [distance.euclidean(posi, (0, 0))*(0.25/3.82) for posi in posilist_array]


def get_convexhull(posilist):
    posilist_array = displayposi_to_array(posilist)
    hull = get_hull(posilist_array)
    return round(hull.area*(0.25/3.82),2)


def get_occupancy_area(posilist):
    posilist_array = displayposi_to_array(posilist)
    hull = get_hull(posilist_array)
    return round(hull.volume*(((0.25/3.82)**2)),2)


def cal_averge_eccentricity(posilist):
    all_eccentricity = get_all_eccentricity(posilist)
    return cal_average(all_eccentricity)


def get_average_spacing(posilist):
    posilist_array = displayposi_to_array(posilist)
    distances =[distance.euclidean(p1,p2) for p1, p2 in combinations(posilist_array,2)]
    return round(sum(distances)/len(distances)*(0.25/3.82),2)


if __name__ == "__main__":
    test = False
    if test:
        posilist = [(20, 0), (25, 5), (100, 75), (50, 50), (-75, 65)]

        a = get_convexhull(posilist)
        b = get_occupancy_area(posilist)
        c = cal_averge_eccentricity(posilist)
        d = get_average_spacing(posilist)

        print("convexhull is", a, ";", "occupancy area is", b, ";", "average eccentricity is", c, ";", "and average spacing is", d)


