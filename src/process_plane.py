import random
from ellipse import Ellipse, Orientation
from allpositions import AllPositions
from scipy.spatial import distance

from src.common.process_basic_data_structure import get_random_item_from_list
from src.draw_displays import drawEllipse_full


def __get_major_axis(ellipse_center_posi: tuple, weight = 0.25) -> float:
    return weight * distance.euclidean(ellipse_center_posi, (0, 0))


def __get_minor_axis(ellipse_center_posi: tuple, weight = 0.1) -> float:
    return weight * distance.euclidean(ellipse_center_posi, (0, 0))


def get_display(full_posi_list: list, protect_zone_ori = Orientation.Both):

    ini_posi = get_random_item_from_list(full_posi_list)

    taken_posi_list = [ini_posi]
    ini_ellipse = Ellipse(ellipse_center_coordinate = ini_posi,
                          ka = __get_major_axis(ini_posi),
                          kb = __get_minor_axis(ini_posi),
                          orientation = protect_zone_ori)
    e_polygone_list = [ini_ellipse]

    # shuffle the position list
    random.shuffle(full_posi_list)

    for posi in full_posi_list:
        elipse = Ellipse(ellipse_center_coordinate = posi,
                         ka = __get_major_axis(posi),
                         kb = __get_minor_axis(posi),
                         orientation = protect_zone_ori)
        if not elipse.is_intersect_multi_polygon(e_polygone_list):
            e_polygone_list.append(elipse)
            taken_posi_list.append(posi)
    return taken_posi_list


if __name__ == '__main__':
    debug = True
    if debug:
        list_t = [(-20, 20), (35, 130), (-45, 50), (-89, -120)]
        posi = get_random_item_from_list(list_t)
        a = __get_major_axis(posi)

        curr_winsize = 0.6
        all_posi_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
        full_posi_list = all_posi_object.get_all_posi_in_winsize(winsize = curr_winsize)
        posis = get_display(full_posi_list, protect_zone_ori = Orientation.Both)
        drawEllipse_full(posis, [], ka = 0.25, kb = 0.1, ellipseColor_t = "white", ellipseColor_r = "white")

        lst = list()
        for i in range(0, 2):
            lst.append(get_display(full_posi_list, protect_zone_ori = Orientation.Both))
