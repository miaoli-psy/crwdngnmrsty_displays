import pandas as pd

from ellipse import Orientation
from src.allpositions import AllPositions
from src.displays import generate_display_add_one_extra_discs, get_two_extra_posis
from src.process_plane import get_display
from src.properties import Properties

curr_winsize = 0.6

# get all possible positions on the display
all_posis_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)

# fixed base posis:
all_based_posis = get_display(full_posi_list, protect_zone_ori = Orientation.Both)

# 0 - 100% pairs, radial and tangential displays
extra_radial_0_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 0, add_discs_ori = "radial")[1]
extra_radial_25_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 0.25, add_discs_ori = "radial")[1]
extra_radial_50_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 0.5, add_discs_ori = "radial")[1]
extra_radial_75_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 0.75, add_discs_ori = "radial")[1]
extra_radial_100_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 1, add_discs_ori = "radial")[1]
extra_tan_0_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 0, add_discs_ori = "tangential")[1]
extra_tan_25_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 0.25, add_discs_ori = "tangential")[1]
extra_tan_50_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 0.5, add_discs_ori = "tangential")[1]
extra_tan_75_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 0.75, add_discs_ori = "tangential")[1]
extra_tan_100_pairs = generate_display_add_one_extra_discs(based_posis = all_based_posis, percent_pairs = 1, add_discs_ori = "tangential")[1]

# add 2 extra discs

extra_posis_radial = get_two_extra_posis(based_posis = all_based_posis, ori = "radial")
extra_posis_tan = get_two_extra_posis(based_posis = all_based_posis, ori = "tangential")

# save to dataframe
column_names = ["base_posi", "extra_r_0", "extra_r_25", "extra_r_50", "extra_r_75", "extra_r_100",
                "extra_t_0", "extra_t_25", "extra_t_50", "extra_t_75", "extra_t_100",
                "tri_r", "tri_t"]

df = pd.DataFrame(columns = column_names)

df = df.append({"base_posi": all_based_posis,
                "extra_r_0": extra_radial_0_pairs,
                "extra_r_25": extra_radial_25_pairs,
                "extra_r_50": extra_radial_50_pairs,
                "extra_r_75": extra_radial_75_pairs,
                "extra_r_100": extra_radial_100_pairs,
                "extra_t_0": extra_tan_0_pairs,
                "extra_t_25": extra_tan_25_pairs,
                "extra_t_50": extra_tan_50_pairs,
                "extra_t_75": extra_tan_75_pairs,
                "extra_t_100": extra_tan_100_pairs,
                "tri_r": extra_posis_radial,
                "tri_t": extra_posis_tan},
               ignore_index = True)

df.to_csv("demo_posi.csv", index = False)