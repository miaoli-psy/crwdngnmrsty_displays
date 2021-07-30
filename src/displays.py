from allpositions import AllPositions
from ellipse import Orientation
from src.common.process_basic_data_structure import random_split_list
from src.common.process_polygon import polypoint_to_coords
from src.draw_displays import drawEllipse_full
from src.process_plane import get_display, get_close_to_fovea_posi, get_far_from_fovea_posi

curr_winsize = 0.6
protect_zone_ori = Orientation.Both
protect_zone_type = "tangential"
percent_pairs = 0.5

all_posis_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)


def gen_radial_display_pairs(based_posis):
    extra_posis = list()
    close_fovea_posis, far_fovea_posis = random_split_list(based_posis, weight = 0.5)
    for posi in close_fovea_posis:
        extra_posis_point = get_close_to_fovea_posi(posi)
        extra_posis.append(polypoint_to_coords(extra_posis_point))
    for posi in far_fovea_posis:
        extra_posis_point = get_far_from_fovea_posi(posi)
        extra_posis.append(polypoint_to_coords(extra_posis_point))
    return based_posis, extra_posis


if __name__ == '__main__':
    based_posis = get_display(full_posi_list, protect_zone_ori = protect_zone_ori)
    display = gen_radial_display_pairs(based_posis)
    drawEllipse_full(display[0], display[1], ka = 0.25, kb = 0.1, ellipseColor_t = "white", ellipseColor_r = "white")