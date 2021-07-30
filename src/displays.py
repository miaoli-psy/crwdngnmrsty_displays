from allpositions import AllPositions
from ellipse import Orientation
from src.common.process_basic_data_structure import random_split_list, get_diff_between_2_lists
from src.common.process_polygon import polypoint_to_coords
from src.draw_displays import drawEllipse_full
from src.process_plane import get_display, get_close_to_fovea_posi, get_far_from_fovea_posi, get_posi_in_tan_area_a, \
    get_posi_in_tan_area_b
import random

curr_winsize = 0.6
protect_zone_ori = Orientation.Both
protect_zone_type = "tangential"
percent_pairs = 0.5

all_posis_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)


def get_one_extra_random_posis(based_posis, ori = "radial"):
    extra_posis = list()
    half_posis_a, half_posis_b = random_split_list(based_posis, weight = 0.5)
    for posi in half_posis_a:
        if ori == "radial":
            extra_posis_point = get_close_to_fovea_posi(posi)
        elif ori == "tangential":
            extra_posis_point = get_posi_in_tan_area_a(posi)
        extra_posis.append(polypoint_to_coords(extra_posis_point))
    for posi in half_posis_b:
        if ori == "radial":
            extra_posis_point = get_far_from_fovea_posi(posi)
        elif ori == "tangential":
            extra_posis_point = get_posi_in_tan_area_b(posi)
        extra_posis.append(polypoint_to_coords(extra_posis_point))
    return extra_posis


def get_two_extra_posis(based_posis, ori = "radial"):
    extra_posis = list()
    for posi in based_posis:
        if ori == "radial":
            point = get_close_to_fovea_posi(posi)
            extra_posis.append(polypoint_to_coords(point))
            point = get_far_from_fovea_posi(posi)
            extra_posis.append(polypoint_to_coords(point))
        elif ori == "tangential":
            point = get_posi_in_tan_area_a(posi)
            extra_posis.append(polypoint_to_coords(point))
            point = get_posi_in_tan_area_b(posi)
            extra_posis.append(polypoint_to_coords(point))
    return extra_posis


def gen_display_full_pairs(based_posis, protect_zone_ori = "radial"):
    return based_posis, get_one_extra_random_posis(based_posis, ori = protect_zone_ori)


def gen_display_75p_paris(based_posis, protect_zone_ori = "radial"):
    extra_posis = list()
    # single based disc posis 只有中间一个点
    no_extra_posi_base = random_split_list(based_posis, weight = 0.125)[0]
    # other posis (2 extra posis, and 1 extra posi)
    rest_posis = get_diff_between_2_lists(based_posis, no_extra_posi_base)
    # the number of 2 extra posis == no extra posis
    two_extra_posis_base = random.sample(rest_posis, len(no_extra_posi_base))
    # get 2 extra posis list
    two_extra_posis_list = get_two_extra_posis(based_posis = two_extra_posis_base, ori = protect_zone_ori)
    # get 1 extra posis list
    one_extra_posi_base = get_diff_between_2_lists(rest_posis, two_extra_posis_base)
    extra_posis_list = get_one_extra_random_posis(based_posis = one_extra_posi_base, ori = protect_zone_ori)
    extra_posis = extra_posis + extra_posis_list + two_extra_posis_list

    return based_posis, extra_posis


if __name__ == '__main__':
    based_posis = get_display(full_posi_list, protect_zone_ori = protect_zone_ori)
    display = gen_display_75p_paris(based_posis, protect_zone_ori = "radial")
    drawEllipse_full(display[0], display[1], ka = 0.25, kb = 0.1, ellipseColor_t = "white", ellipseColor_r = "white")