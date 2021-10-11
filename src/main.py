import pandas as pd

from ellipse import Orientation
from src.allpositions import AllPositions
from src.displays import generate_display_add_one_extra_discs
from src.process_plane import get_display
from src.properties import Properties

curr_winsize = 0.4
protect_zone_type = "radial"
percent_pairs = 1
save_to_csv = False

run_n = 500
all_posis_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)
column_names = ["n", "winsize", "numerosity", "allposis", "centralposis", "extraposis", "perceptpairs",
                "protectzonetype", "convexhull", "occupancyarea", "averageeccentricity", "averagespacing",
                "density"]

all_display_df = pd.DataFrame(columns = column_names)
for n in range(1, run_n + 1):
    print(n)
    all_based_posis = get_display(full_posi_list, protect_zone_ori = Orientation.Both)
    my_display = generate_display_add_one_extra_discs(based_posis = all_based_posis,
                                                      percent_pairs = percent_pairs,
                                                      add_discs_ori = protect_zone_type)

    properites = Properties(my_display[0] + my_display[1])

    new_display = {"n":                    n,
                   "winsize":              curr_winsize,
                   "numerosity":           len(my_display[0]) * 2,
                   "allposis":            my_display[0] + my_display[1],
                   "centralposis":        my_display[0],
                   "extraposis":          my_display[1],
                   "perceptpairs":        percent_pairs,
                   "protectzonetype":    protect_zone_type,
                   "convexhull":           properites.convexhull,
                   "occupancyarea":       properites.occupancy_area,
                   "averageeccentricity": properites.averge_eccentricity,
                   "averagespacing":      properites.average_spacing,
                   "density":              properites.density}

    all_display_df = all_display_df.append(new_display, ignore_index = True)

if save_to_csv:
    all_display_df.to_csv("ws%s_%s_%spairs.csv" % (curr_winsize, protect_zone_type, percent_pairs), index = False)
