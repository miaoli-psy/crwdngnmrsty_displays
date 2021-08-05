import pandas as pd

from ellipse import Orientation
from src.allpositions import AllPositions
from src.displays import generate_display_direct_add_extra_discs
from src.process_plane import get_display
from src.properties import Properties


curr_winsize = 0.6
protect_zone_type = "tangential"
percent_pairs = 0.5
run_n = 3
all_posis_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)
all_based_posis = get_display(full_posi_list, protect_zone_ori = Orientation.Both)
column_names = ["n", "all posis", "central posis", "extra posis", "percept pairs", "protect zone type", "convexhull", "occupancy area", "average eccentricity", "average spacing", "density"]

all_display_df = pd.DataFrame(columns = column_names)
for n in range(1, run_n+1):
    my_display = generate_display_direct_add_extra_discs(based_posis = all_based_posis,
                                                         percent_pairs = percent_pairs,
                                                         add_discs_ori = protect_zone_type)

    properites = Properties(my_display[0] + my_display[1])

    new_display = {"n": n,
                   "all posis": my_display[0] + my_display[1],
                   "central posis": my_display[0],
                   "extra posis": my_display[1],
                   "percept pairs": percent_pairs,
                   "protect zone type": protect_zone_type,
                   "convexhull": properites.convexhull,
                   "occupancy area": properites.occupancy_area,
                   "average eccentricity": properites.averge_eccentricity,
                   "average spacing": properites.average_spacing,
                   "density": properites.density}

    all_display_df = all_display_df.append(new_display, ignore_index = True)




