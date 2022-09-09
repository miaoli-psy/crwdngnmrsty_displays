import pandas as pd
import numpy as np
from scipy.spatial import distance, ConvexHull
from itertools import combinations

from src.common.process_basic_data_structure import cal_average
from src.common.process_dataframe import process_col, insert_new_col_from_two_cols
from src.common.process_str import str_to_list


def __get_display_hull(posis):
    return ConvexHull(np.asarray(posis))


def get_display_convexhull(posis, pix_to_deg = 0.04):
    hull = __get_display_hull(posis)
    return round(hull.area * pix_to_deg, 2)


def get_display_occupancyarea(posis, pix_to_deg = 0.04):
    hull = __get_display_hull(posis)
    return round(hull.volume * pix_to_deg ** 2, 2)


def get_display_avg_e(posis, pix_to_deg = 0.04):
    posi_array = np.asarray(posis)
    all_e = [distance.euclidean(posi, (0, 0)) * pix_to_deg for posi in posi_array]
    return cal_average(all_e)


def get_density(numerosity, occupancy_area):
    return round(numerosity / occupancy_area, 4)


def get_average_spacing(posis, pix_to_deg = 0.04):
    posi_array = np.asarray(posis)
    distances = [distance.euclidean(p1, p2) for p1, p2 in combinations(posi_array, 2)]
    return round(sum(distances) / len(distances) * pix_to_deg, 2)


if __name__ == '__main__':
    write_to_excel = False
    PATH = "../../selected_display/"
    FILE = "ms2_displays_triplets.xlsx"

    # read display file
    displays = pd.read_excel(PATH + FILE)

    # positions, remove str formate
    process_col(displays, "allposis", str_to_list)

    # cal properties
    insert_new_col_from_two_cols(displays, "allposis", "pix_to_deg_index", "convex", get_display_convexhull)
    insert_new_col_from_two_cols(displays, "allposis", "pix_to_deg_index", "occu", get_display_occupancyarea)
    insert_new_col_from_two_cols(displays, "numerosity", "occu", "den", get_density)
    insert_new_col_from_two_cols(displays, "allposis", "pix_to_deg_index", "e", get_display_avg_e)
    insert_new_col_from_two_cols(displays, "allposis", "pix_to_deg_index", "spacing", get_average_spacing)

    if write_to_excel:
        displays.to_excel("displays.xlsx", index = False)
