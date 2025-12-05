from allpositions import AllPositions
from ellipse import Orientation
from src.common.process_basic_data_structure import random_split_list, get_diff_between_2_lists
from src.common.process_polygon import polypoint_to_coords
from src.draw_displays import drawEllipse_full, draw_disc_only, drawEllipses
from src.process_plane import get_display, get_close_to_fovea_posi, get_far_from_fovea_posi, get_posi_in_tan_area_a, \
    get_posi_in_tan_area_b
import random


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


def get_two_extra_posis(based_posis, ori = "radial", radial_weight=0.25, tan_weight=0.1):
    extra_posis = list()
    for posi in based_posis:
        if ori == "radial":
            point = get_close_to_fovea_posi(posi,radial_weight, tan_weight)
            extra_posis.append(polypoint_to_coords(point))
            point = get_far_from_fovea_posi(posi,radial_weight, tan_weight)
            extra_posis.append(polypoint_to_coords(point))
        elif ori == "tangential":
            point = get_posi_in_tan_area_a(posi,radial_weight, tan_weight)
            extra_posis.append(polypoint_to_coords(point))
            point = get_posi_in_tan_area_b(posi,radial_weight, tan_weight)
            extra_posis.append(polypoint_to_coords(point))
    return extra_posis


def get_no_extra_posi_base(based_posis, percent_pairs):
    if percent_pairs == 0.75:
        no_extra_posi_base = random_split_list(based_posis, weight = 0.125)[0]
    elif percent_pairs == 0.5:
        no_extra_posi_base = random_split_list(based_posis, weight = 0.25)[0]
    elif percent_pairs == 0.25:
        no_extra_posi_base = random_split_list(based_posis, weight = 0.375)[0]
    elif percent_pairs == 0:
        no_extra_posi_base = random_split_list(based_posis, weight = 0.5)[0]
    else:
        no_extra_posi_base = random_split_list(based_posis, weight = 0.25)[0]
        print(f"warning, percent_pairs == {percent_pairs} is not support, generate displays with 50% pairs. Only "
              f"support 0, 0.25，0.5, 0.75")
    return no_extra_posi_base


def generate_display_add_one_extra_discs(based_posis, percent_pairs = 1.0, add_discs_ori = "radial"):
    if percent_pairs == 1.0:
        return based_posis, get_one_extra_random_posis(based_posis, ori = add_discs_ori)
    else:
        extra_posis = list()
        # single based disc posis 只有中间一个点
        no_extra_posi_base = get_no_extra_posi_base(based_posis = based_posis, percent_pairs = percent_pairs)
        # other posis (2 extra posis, and 1 extra posi)
        rest_posis = get_diff_between_2_lists(based_posis, no_extra_posi_base)
        # the number of 2 extra posis == no extra posis
        two_extra_posis_base = random.sample(rest_posis, len(no_extra_posi_base))
        # get 2 extra posis list
        two_extra_posis_list = get_two_extra_posis(based_posis = two_extra_posis_base, ori = add_discs_ori)
        # get 1 extra posis list
        one_extra_posi_base = get_diff_between_2_lists(rest_posis, two_extra_posis_base)
        extra_posis_list = get_one_extra_random_posis(based_posis = one_extra_posi_base, ori = add_discs_ori)
        extra_posis = extra_posis + extra_posis_list + two_extra_posis_list

        return based_posis, extra_posis


if __name__ == '__main__':
    debug = False
    savefig = True

    curr_winsize = 0.6
    protect_zone_ori = Orientation.Both
    protect_zone_type = "radial"
    # protect_zone_type = "tangential"
    all_triplet = True
    percent_pairs = 0
    if debug:
        all_posis_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
        full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)
        all_based_posis = get_display(full_posi_list, protect_zone_ori = protect_zone_ori)
        if all_triplet:
            extras = get_two_extra_posis(based_posis = all_based_posis, ori = protect_zone_type)
            display = [all_based_posis, extras]
        else:
            display = generate_display_add_one_extra_discs(all_based_posis, percent_pairs = percent_pairs, add_discs_ori = protect_zone_type)

        drawEllipse_full(display[0], display[1], ka = 0.25, kb = 0.1, ellipseColor_t = "white",
                         ellipseColor_r = "white", savefig = savefig)
        # drawEllipses(all_based_posis, ka = 0.1, kb = 0.25, ellipseColor = "white", extra_posi = extras)
        draw_disc_only(display[0], display[1], contrast = False, savefig = savefig)

    try_signle_ori = True

    if try_signle_ori:
        signal_ori = Orientation.Radial
        all_posis_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
        full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)
        all_based_posis = get_display(full_posi_list, protect_zone_ori = signal_ori)

        tan_all_posis = [(-210.0, -60.0), (-180.0, -210.0), (-200.0, 40.0), (20.0, 110.0), (-80.0, 90.0), (-90.0, -120.0), (130.0, 140.0), (0.0, 150.0), (250.0, 100.0), (-270.0, -170.0), (100.0, -130.0), (-200.0, 160.0), (-130.0, -70.0), (-50.0, -170.0), (290.0, 10.0), (200.0, -170.0), (300.0, -110.0), (-120.0, 170.0), (-50.0, 200.0), (280.0, 210.0), (130.0, -20.0), (100.0, -60.0), (30.0, -140.0), (150.0, 80.0), (-120.0, -20.0), (70.0, -210.0), (-290.0, 120.0), (80.0, 130.0), (90.0, 70.0), (-270.0, -20.0), (70.0, 200.0), (-120.0, 80.0), (180.0, -100.0), (-10.0, -190.0), (230.0, -40.0), (100.0, 40.0), (160.0, 40.0), (-40.0, 110.0), (-90.0, -80.0), (-20.0, -100.0), (50.0, -110.0), (-100.0, 20.0), (-110.0, -220.0), (130.0, -220.0), (130.0, 220.0), (-50.0, -100.0), (-130.0, 50.0), (100.0, 10.0), (-160.0, -130.0)]
        rad_all_posis = [(-170.0, -60.0), (70.0, 120.0), (230.0, 30.0), (-130.0, -180.0), (-60.0, -90.0), (260.0, -180.0), (270.0, 80.0), (-280.0, 150.0), (50.0, -210.0), (-180.0, 90.0), (120.0, -150.0), (-110.0, -30.0), (-300.0, -140.0), (160.0, 110.0), (30.0, -120.0), (-260.0, -10.0), (-40.0, -160.0), (-130.0, 200.0), (100.0, -70.0), (60.0, 80.0), (160.0, -210.0), (100.0, -10.0), (-110.0, 70.0), (-50.0, 120.0), (170.0, -30.0), (-140.0, 80.0), (-190.0, -210.0), (130.0, 70.0), (140.0, -10.0), (100.0, -110.0), (0.0, 180.0), (260.0, 220.0), (-140.0, -40.0), (-20.0, 100.0), (90.0, 210.0), (-100.0, 20.0), (-80.0, 70.0), (230.0, -100.0), (-10.0, -100.0), (-110.0, 150.0), (80.0, 150.0), (-60.0, -120.0), (180.0, 210.0), (40.0, -170.0), (110.0, 50.0), (60.0, -80.0), (-220.0, 120.0), (-110.0, -120.0), (-20.0, 220.0)]

        tan_all_posis50 = [(170.0, -70.0), (160.0, 90.0), (-150.0, -120.0), (30.0, 110.0), (-30.0, 100.0), (250.0, 70.0), (-130.0, -200.0), (-220.0, -70.0), (100.0, 120.0), (-110.0, 200.0), (-290.0, 20.0), (100.0, 200.0), (0.0, -180.0), (200.0, -190.0), (190.0, 200.0), (-60.0, -170.0), (-100.0, 70.0), (-170.0, -20.0), (-240.0, 80.0), (-40.0, 210.0), (-110.0, 120.0), (280.0, -50.0), (-280.0, -220.0), (-130.0, -60.0), (40.0, 190.0), (-220.0, 160.0), (-60.0, 100.0), (-110.0, 20.0), (240.0, -140.0), (0.0, 110.0), (170.0, 20.0), (50.0, -140.0), (70.0, -100.0), (130.0, -90.0), (120.0, -190.0), (90.0, 70.0), (120.0, 40.0), (280.0, 200.0), (110.0, -20.0), (-130.0, 50.0), (290.0, 10.0), (-80.0, -110.0), (-30.0, -100.0), (0.0, -100.0), (50.0, 90.0), (-200.0, 220.0), (-100.0, -20.0), (100.0, 10.0), (50.0, -220.0), (-80.0, -60.0)]
        rad_all_posis50 =[(-170.0, 140.0), (-220.0, -220.0), (-240.0, 110.0), (280.0, 60.0), (-140.0, -160.0), (110.0, -10.0), (-110.0, 220.0), (-80.0, -140.0), (-40.0, -200.0), (150.0, -220.0), (260.0, -180.0), (120.0, 190.0), (-270.0, -50.0), (220.0, 20.0), (-110.0, 40.0), (100.0, 130.0), (-40.0, 120.0), (80.0, -130.0), (-50.0, 150.0), (0.0, -110.0), (-100.0, -20.0), (140.0, -80.0), (-210.0, -70.0), (200.0, -90.0), (-30.0, 200.0), (290.0, 170.0), (-130.0, 100.0), (170.0, 30.0), (-270.0, 210.0), (190.0, 200.0), (-160.0, -50.0), (70.0, 110.0), (110.0, 60.0), (60.0, -210.0), (120.0, -150.0), (20.0, -170.0), (140.0, -10.0), (0.0, 100.0), (-130.0, -10.0), (-60.0, 80.0), (-90.0, -90.0), (-30.0, -130.0), (50.0, 90.0), (-200.0, 30.0), (-60.0, -80.0), (80.0, -70.0), (170.0, 110.0), (30.0, 170.0), (260.0, -70.0), (110.0, -70.0)]

        tan_all_51 = [(300.0, -10.0), (-230.0, -50.0), (10.0, -140.0), (-60.0, -220.0), (-190.0, -140.0), (-90.0, 210.0), (20.0, 140.0), (290.0, 130.0), (-120.0, -150.0), (230.0, 40.0), (-160.0, 220.0), (300.0, -170.0), (-30.0, 130.0), (100.0, 20.0), (110.0, 80.0), (-120.0, 90.0), (80.0, 150.0), (160.0, 210.0), (-300.0, -160.0), (50.0, -150.0), (210.0, 150.0), (210.0, -180.0), (100.0, -70.0), (230.0, -80.0), (-240.0, 60.0), (-50.0, -90.0), (110.0, -140.0), (130.0, 50.0), (-260.0, 160.0), (170.0, -30.0), (-110.0, -30.0), (-100.0, -80.0), (-50.0, 100.0), (70.0, 80.0), (-210.0, 0.0), (-130.0, 20.0), (60.0, 220.0), (130.0, -50.0), (-160.0, -70.0), (-20.0, 210.0), (-150.0, 60.0), (-110.0, -210.0), (-80.0, 100.0), (170.0, -100.0), (-30.0, -130.0), (-10.0, -220.0), (110.0, -220.0), (40.0, 110.0), (120.0, 0.0), (60.0, -100.0), (100.0, -20.0)]
        rad_all_51 = [(220.0, 110.0), (-60.0, -80.0), (-220.0, -190.0), (-170.0, 0.0), (50.0, -110.0), (-240.0, 20.0), (-90.0, -180.0), (250.0, -90.0), (20.0, 200.0), (80.0, 150.0), (270.0, 180.0), (140.0, 160.0), (160.0, -220.0), (-200.0, 140.0), (-110.0, 70.0), (120.0, 50.0), (150.0, -90.0), (-190.0, -80.0), (-30.0, 160.0), (-290.0, -50.0), (110.0, -70.0), (-110.0, 140.0), (-80.0, 210.0), (70.0, -200.0), (10.0, 110.0), (-30.0, -150.0), (80.0, 80.0), (-10.0, -110.0), (-140.0, -70.0), (190.0, -110.0), (130.0, 90.0), (-250.0, 210.0), (260.0, -190.0), (200.0, 10.0), (100.0, 30.0), (140.0, 220.0), (-100.0, -60.0), (-190.0, 70.0), (-60.0, -110.0), (50.0, -140.0), (-50.0, 110.0), (-290.0, -220.0), (-120.0, -220.0), (-130.0, -10.0), (160.0, 10.0), (-100.0, -10.0), (110.0, -20.0), (-80.0, 60.0), (290.0, 30.0), (40.0, 130.0), (80.0, -60.0)]


        color_list = ["#DCDCDC",
                      "#E3E3E3",
                      "#E9E9E9",
                      "#EDEDED",
                      "#F1F1F1",
                      "#F4F4F4",
                      "#F6F6F6",
                      "#F8F8F8",
                      "#F9F9F9",
                      "#FFFFFF"]

        for color in color_list:
            drawEllipses(posi = tan_all_posis50,
                         ka = 0.25,
                         kb = 0.1,
                         ellipseColor = color,
                         ellipsetransp = 0.5,
                         extra_posi = [],
                         extra_disc_color = 'orangered',
                         savefig = savefig)

        draw_disc_only(e_posi_base = rad_all_51,
                       e_posi_extra = [],
                       savefig = savefig)


