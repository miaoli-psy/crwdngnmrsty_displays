import pandas as pd

from ellipse import Orientation
from src.allpositions import AllPositions
from src.displays import generate_display_add_one_extra_discs
from src.process_plane import get_display
from src.properties import Properties

curr_winsize = 0.4
protect_zone_type = "circle"
save_to_csv = False
radial_weight = 0.15
tan_weight = 0.15

run_n = 5000
all_posis_object = AllPositions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
full_posi_list = all_posis_object.get_all_posi_in_winsize(winsize = curr_winsize)
column_names = ["n", "winsize", "numerosity", "all posis", "extra posis", "protect zone type", "convexhull",
                "occupancy area", "average eccentricity", "average spacing", "density", "radius"]

all_display_df = pd.DataFrame(columns = column_names)
for n in range(1, run_n + 1):
    print(n)
    all_based_posis = get_display(full_posi_list, protect_zone_ori = Orientation.Radial,
                                  radial_weight = radial_weight, tan_weight = tan_weight)

    properites = Properties(all_based_posis)

    new_display = {"n":                    n,
                   "winsize":              curr_winsize,
                   "numerosity":           len(all_based_posis),
                   "all posis":            all_based_posis,
                   "protect zone type":    protect_zone_type,
                   "convexhull":           properites.convexhull,
                   "occupancy area":       properites.occupancy_area,
                   "average eccentricity": properites.averge_eccentricity,
                   "average spacing":      properites.average_spacing,
                   "density":              properites.density,
                   "radius":               radial_weight}

    all_display_df = all_display_df.append(new_display, ignore_index = True)

if save_to_csv:
    all_display_df.to_csv("ws%s_%s_%s.csv" % (curr_winsize, protect_zone_type, radial_weight), index = False)