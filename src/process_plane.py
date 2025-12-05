import math
import random
from ellipse import Ellipse, Orientation
from allpositions import AllPositions
from scipy.spatial import distance
from shapely.geometry import Point
from shapely import affinity

from src.common.process_basic_data_structure import get_random_item_from_list
from src.common.process_polygon import get_intersect_poly, get_random_point_in_polygon, plot_polygon
from src.draw_displays import drawEllipse_full


def __get_major_axis(ellipse_center_posi: tuple, weight=0.25) -> float:
    return weight * distance.euclidean(ellipse_center_posi, (0, 0))


def __get_minor_axis(ellipse_center_posi: tuple, weight=0.1) -> float:
    return weight * distance.euclidean(ellipse_center_posi, (0, 0))


def euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def get_display(full_posi_list: list, protect_zone_ori=Orientation.Both, radial_weight=0.25,
                tan_weight=0.1):
    ini_posi = get_random_item_from_list(full_posi_list)

    # 初始化起始点
    taken_posi_list = [ini_posi]
    ini_ellipse = Ellipse(ellipse_center_coordinate=ini_posi,
                          ka=__get_major_axis(ini_posi, weight=radial_weight),
                          kb=__get_minor_axis(ini_posi, weight=tan_weight),
                          orientation=protect_zone_ori)
    e_polygone_list = [ini_ellipse]

    # shuffle the position list
    random.shuffle(full_posi_list)

    # 遍历每个点进行测试

    for posi in full_posi_list:
        if posi in taken_posi_list:
            continue
        dist1 = math.hypot(posi[0], posi[1])

        # Step 3.1: 早跳过逻辑（减少 ellipse 构造）
        skip = False
        for taken in taken_posi_list:
            dist2 = math.hypot(taken[0], taken[1])  # 已有点到（0， 0）距离
            min_allow_dist = radial_weight * (dist1 + dist2)
            if euclidean_distance(posi, taken) < min_allow_dist:
                skip = True
                break
        if skip:
            continue

        elipse = Ellipse(ellipse_center_coordinate=posi,
                         ka=__get_major_axis(posi, weight=radial_weight),
                         kb=__get_minor_axis(posi, weight=tan_weight),
                         orientation=protect_zone_ori)

        if not elipse.is_intersect_multi_polygon(e_polygone_list):
            e_polygone_list.append(elipse)
            taken_posi_list.append(posi)

    return taken_posi_list


def get_close_to_fovea_posi(posi, radial_weight=0.25, tan_weight=0.1):
    radial_ellipse_poly = Ellipse(ellipse_center_coordinate=posi,
                                  ka=__get_major_axis(posi, weight=radial_weight),
                                  kb=__get_minor_axis(posi, weight=tan_weight),
                                  orientation=Orientation.Radial).polygon

    tangential_ellipse_poly = Ellipse(ellipse_center_coordinate=posi,
                                      ka=__get_major_axis(posi, weight=radial_weight),
                                      kb=__get_minor_axis(posi, weight=tan_weight),
                                      orientation=Orientation.Tangential).polygon

    intersect = get_intersect_poly(radial_ellipse_poly, tangential_ellipse_poly)

    while True:
        point = get_random_point_in_polygon(radial_ellipse_poly)
        if not point.within(intersect):
            if point.distance(Point(0, 0)) < Point(posi).distance(Point(0, 0)):
                return point


def get_far_from_fovea_posi(posi, radial_weight=0.25, tan_weight=0.1):
    point = get_close_to_fovea_posi(posi, radial_weight, tan_weight)
    return affinity.rotate(point, 180, origin=Point(posi))


def get_posi_in_tan_area_a(posi, radial_weight=0.25, tan_weight=0.1):
    # 如 posi 在第一象限，此点靠近 x 轴（逆时针转 90 度）
    point = get_close_to_fovea_posi(posi, radial_weight, tan_weight)
    return affinity.rotate(point, 90, origin=Point(posi))


def get_posi_in_tan_area_b(posi, radial_weight=0.25, tan_weight=0.1):
    point = get_close_to_fovea_posi(posi, radial_weight, tan_weight)
    return affinity.rotate(point, 270, origin=Point(posi))


if __name__ == '__main__':
    debug = True
    if debug:
        list_t = [(-20, 20), (35, 130), (-45, 50), (-89, -120)]
        posi = get_random_item_from_list(list_t)

        curr_winsize = 0.6
        radial_weight = 0.15
        tan_weight = 0.15
        all_posi_object = AllPositions(grid_x=101, grid_y=75, line_length=10, fovea_radius=100)
        full_posi_list = all_posi_object.get_all_posi_in_winsize(winsize=curr_winsize)
        posis = get_display(full_posi_list, protect_zone_ori=Orientation.Radial,
                            radial_weight=radial_weight, tan_weight=tan_weight)
        drawEllipse_full(posis, [], ka=radial_weight, kb=tan_weight, ellipseColor_t="white",
                         ellipseColor_r="white")

        lst = list()
        for i in range(0, 2):
            lst.append(get_display(full_posi_list, protect_zone_ori=Orientation.Both))

        extra_posi_list = list()

        for posi in posis:
            point = get_close_to_fovea_posi(posi)
            extra_posi_list.append(list(point.coords)[0])

        test_e_poly = Ellipse(posi, __get_minor_axis(posi), __get_major_axis(posi),
                              orientation=Orientation.Radial).polygon
        toplot = [test_e_poly, get_posi_in_tan_area_a(posi).buffer(0.5)]

        plot_polygon(toplot, axes_lim=[-150, 150])
