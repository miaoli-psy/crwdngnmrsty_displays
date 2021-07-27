from scipy.spatial import distance, ConvexHull
from itertools import combinations
import numpy as np

from src.common.process_basic_data_structure import cal_average


class Properties:
    def __init__(self, posilist):
        self.__posilist_array = np.asarray(posilist)
        self.__hull = ConvexHull(self.__posilist_array)
        self.convexhull = round(self.__hull.area * (0.25 / 3.82), 2)
        self.occupancy_area = round(self.__hull.volume * ((0.25 / 3.82) ** 2), 2)
        self.averge_eccentricity = self.cal_averge_eccentricity()
        self.average_spacing = self.get_average_spacing()
        self.density = round(len(posilist)/self.occupancy_area, 4)

    def cal_averge_eccentricity(self):
        all_eccentricity = [distance.euclidean(posi, (0, 0)) * (0.25 / 3.82) for posi in self.__posilist_array]
        return cal_average(all_eccentricity)

    def get_average_spacing(self):
        distances = [distance.euclidean(p1, p2) for p1, p2 in combinations(self.__posilist_array, 2)]
        return round(sum(distances) / len(distances) * (0.25 / 3.82), 2)


if __name__ == "__main__":
    debug = True
    if debug:
        properties = Properties([(20, 0), (25, 5), (100, 75), (50, 50), (-75, 65)])
        a = properties.convexhull
        b = properties.occupancy_area
        c = properties.averge_eccentricity
        d = properties.average_spacing
        e = properties.density
        print("convexhull is", a, ";", "occupancy area is", b, ";", "average eccentricity is", c, ";",
              "and average spacing is", d, "density is", e, "item/cm2")