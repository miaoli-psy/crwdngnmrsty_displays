import random
from ellipse import Ellipse, Orientation
from positions import Positions
from scipy.spatial import distance

from src.draw_displays import drawEllipse_full, drawEllipses


def get_random_posi(posilist: list) -> tuple:
    return random.choice(posilist)


def get_major_axis(ellipse_center_posi: tuple, weight = 0.25) -> float:
    return weight * distance.euclidean(ellipse_center_posi, (0, 0))


def get_minor_axis(ellipse_center_posi: tuple, weight = 0.1) -> float:
    return weight * distance.euclidean(ellipse_center_posi, (0, 0))


def get_display(winsize = 0.6, orientation = Orientation.Both):
    full_posi_list = Positions().get_all_posi_in_winsize(winsize = winsize)
    ini_posi = get_random_posi(full_posi_list)

    taken_posi_list = [ini_posi]
    ini_ellipse = Ellipse(ellipse_center_coordinate = ini_posi,
                          ka = get_major_axis(ini_posi),
                          kb = get_minor_axis(ini_posi),
                          orientation = orientation)
    e_polygone_list = [ini_ellipse]

    for posi in full_posi_list:
        elipse = Ellipse(ellipse_center_coordinate = posi,
                         ka = get_major_axis(posi),
                         kb = get_minor_axis(posi),
                         orientation = orientation)
        if not elipse.is_intersect_multi_polygon(e_polygone_list):
            e_polygone_list.append(elipse)
            taken_posi_list.append(posi)
    return taken_posi_list


if __name__ == '__main__':
    debug = True
    if debug:
        list = [(-20, 20), (35, 130), (-45, 50), (-89, -120)]
        posi = get_random_posi(list)
        a = get_major_axis(posi)
        posis = get_display()
        drawEllipses(posis, ka = 0.25, kb = 0.1, ellipseColor = "white")