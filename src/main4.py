"""
select N random positions from a given position lists
to get displays with numerosity N
"""
import random
import pandas as pd

from src.allpositions import AllPositions
from src.properties import Properties

curr_winsize = 0.5
save_to_csv = True

run_n = 1000
numerosity = 16

all_posis_object = AllPositions(grid_x = 75, grid_y = 75, line_length = 10, fovea_radius = 2)
full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)

column_names = ["n", "winsize", "numerosity", "allposis",  "convexhull",
                "occupancyarea", "averageeccentricity", "averagespacing", "density"]

all_display_df = pd.DataFrame(columns = column_names)

for n in range(1, run_n + 1):
    print(n)

    my_posis = random.sample(full_posi_list, numerosity)

    properites = Properties(my_posis)

    new_display = {"n": n,
                   "winsize": curr_winsize,
                   "numerosity": numerosity,
                   "allposis": my_posis,
                   "convexhull": properites.convexhull,
                   "occupancyarea": properites.occupancy_area,
                   "averageeccentricity": properites.averge_eccentricity,
                   "averagespacing": properites.average_spacing,
                   "density": properites.density}

    all_display_df = all_display_df.append(new_display, ignore_index = True)

if save_to_csv:
    all_display_df.to_csv("n%s_%s.csv" % (n, numerosity), index = False)