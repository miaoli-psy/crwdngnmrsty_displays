from scipy.spatial import distance, ConvexHull
from itertools import combinations
import numpy as np

from src.common.process_basic_data_structure import cal_average


class Properties:
    def __init__(self, posilist, pix_to_deg = 0.04):
        self.__posilist_array = np.asarray(posilist)
        self.__hull = ConvexHull(self.__posilist_array)
        self.pix_to_deg_index = pix_to_deg
        # self.convexhull = round(self.__hull.area * (0.25 / 3.82), 2)
        self.convexhull = round(self.__hull.area * pix_to_deg, 2)
        # self.occupancy_area = round(self.__hull.volume * ((0.25 / 3.82) ** 2), 2)
        self.occupancy_area = round(self.__hull.volume * pix_to_deg ** 2, 2)
        self.averge_eccentricity = self.cal_averge_eccentricity()
        self.average_spacing = self.get_average_spacing()
        self.density = round(len(posilist) / self.occupancy_area, 4)
        self.numerosity = len(posilist)

    def cal_averge_eccentricity(self):
        all_eccentricity = [distance.euclidean(posi, (0, 0)) * self.pix_to_deg_index for posi in self.__posilist_array]
        return cal_average(all_eccentricity)

    def get_average_spacing(self, pix_to_deg_index = 0.04):
        distances = [distance.euclidean(p1, p2) for p1, p2 in combinations(self.__posilist_array, 2)]
        return round(sum(distances) / len(distances) * pix_to_deg_index, 2)


if __name__ == "__main__":
    debug = True
    if debug:
        # properties = Properties([(10, 10), (10, -10), (-10, -10), (-10, 10)])
        properties = Properties(
                [(50.0, 240.0), (-160.0, -180.0), (-340.0, 80.0), (160.0, -40.0), (100.0, -10.0), (330.0, -200.0),
                 (200.0, -90.0), (130.0, -120.0), (-70.0, 220.0), (0.0, -170.0), (40.0, -110.0), (250.0, -130.0),
                 (120.0, 140.0), (350.0, 50.0), (40.0, -230.0), (-250.0, 130.0), (-230.0, 40.0), (-170.0, 60.0),
                 (-130.0, -140.0), (220.0, 60.0), (310.0, 220.0), (-350.0, -180.0), (260.0, 150.0), (-110.0, 110.0),
                 (-190.0, -60.0), (-290.0, -20.0), (-260.0, -170.0), (150.0, 40.0), (0.0, 160.0), (-130.0, 250.0),
                 (130.0, -10.0), (-120.0, 0.0), (-310.0, 240.0), (210.0, -250.0), (-140.0, 140.0), (-80.0, -90.0),
                 (100.0, 40.0), (-120.0, -100.0), (50.0, 120.0), (-10.0, -130.0), (110.0, -80.0), (20.0, 100.0),
                 (-80.0, 80.0), (-50.0, -200.0), (150.0, 250.0), (-30.0, -100.0), (80.0, -70.0), (290.0, 10.0),
                 (150.0, 170.0), (150.0, -200.0), (110.0, 70.0), (-90.0, -50.0), (20.0, 200.0), (-230.0, -80.0),
                 (-160.0, -30.0), (-30.0, 110.0), (60.0, -130.0), (-130.0, 50.0)])
        # properties = Properties([(-60.0, 110.0), (-40.0, -140.0), (-110.0, -100.0), (150.0, 120.0), (100.0, 0.0), (80.0, -100.0), (160.0, 20.0), (-140.0, -10.0), (-100.0, 60.0), (80.0, 140.0), (-60.0, -80.0), (140.0, -90.0), (-180.0, 100.0), (-180.0, -70.0), (20.0, 130.0), (10.0, -120.0), (90.0, 60.0), (13.869669861558279, 146.89501112823876), (-147.9282430984944, -60.85874020783034), (-202.85285142413292, -76.67353758279815), (-81.5215921310935, 53.08960239872458), (-107.61141918831316, 74.91249783802625), (65.27087696180456, 127.52466778633799), (101.47617442077376, 163.7027887149124), (-49.20870058772314, -62.50495011433299), (-66.13249432305611, -89.95369188913578), (-166.89740847346724, 73.28482429982635), (-221.09970576843705, 117.09043033747047), (72.58696938760912, 47.30007380296372), (94.40993752556054, 73.96100383648456), (106.4011862177574, -69.33862450164787), (162.37089759633838, -87.77998467767904), (6.920053215475432, -99.89364965684928), (18.581399229647584, -142.02060117094493)])
        a = properties.convexhull
        b = properties.occupancy_area
        c = properties.averge_eccentricity
        d = properties.average_spacing
        e = properties.density
        f = properties.numerosity
        print("convexhull is", a, ";", "occupancy area is", b, ";", "average eccentricity is", c, ";",
              "and average spacing is", d, "density is", e, "item/cm2", ";", "numerosity", f)
