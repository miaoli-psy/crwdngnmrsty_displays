import pandas as pd

from ellipse import Orientation
from src.allpositions import AllPositions
from src.displays import generate_display_add_one_extra_discs, get_two_extra_posis
from src.process_plane import get_display
from src.properties import Properties

curr_winsize = 0.4
protect_zone_type = "radial"
save_to_csv = True

run_n = 5
all_posis_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)
column_names = ["n", "winsize", "numerosity", "allposis", "centralposis", "extraposis", "protectzonetype",
                "convexhull", "occupancyarea", "averageeccentricity", "averagespacing", "density"]

all_display_df = pd.DataFrame(columns = column_names)
for n in range(1, run_n + 1):
    print(n)
    all_based_posis = get_display(full_posi_list, protect_zone_ori = Orientation.Both)

    extra_posis = get_two_extra_posis(based_posis = all_based_posis, ori = protect_zone_type)

    my_display = [all_based_posis, extra_posis]

    properites = Properties(my_display[0] + my_display[1])

    new_display = {"n":                   n,
                   "winsize":             curr_winsize,
                   "numerosity":          len(my_display[0]) * 3,
                   "allposis":            my_display[0] + my_display[1],
                   "centralposis":        my_display[0],
                   "extraposis":          my_display[1],
                   "protectzonetype":     protect_zone_type,
                   "convexhull":          properites.convexhull,
                   "occupancyarea":       properites.occupancy_area,
                   "averageeccentricity": properites.averge_eccentricity,
                   "averagespacing":      properites.average_spacing,
                   "density":             properites.density}

    all_display_df = all_display_df.append(new_display, ignore_index = True)

if save_to_csv:
    all_display_df.to_csv("ws%s_%striplets.csv" % (curr_winsize, protect_zone_type), index = False)
