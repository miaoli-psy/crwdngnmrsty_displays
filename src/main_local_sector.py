import random
import pandas as pd
from ellipse import Ellipse, Orientation
from src.process_plane import get_display
from src.draw_displays import drawEllipse_full, draw_disc_only, drawEllipses
from src.displays import generate_display_add_one_extra_discs, get_two_extra_posis

from src.allpositions import AllPositions_full
from src.properties import Properties


curr_winsize = 0.6
sector_angle = 90 # 0-360
direction = 0 # 0-360
fovea_radius = 200
radial_weight = 0.25
tangential_weight = 0.1
protect_zone_type = "radial"
# protect_zone_type = "tangential"
save_to_csv = True
demo_plots = True
run_n = 10

all_posis_Object = AllPositions_full(width = 1920, height = 1080, fovea_radius = 200, window_size = curr_winsize)
full_posi_list = all_posis_Object.generate_sector_posi(angle_deg = sector_angle, direction_deg = direction)


column_names = ["n", "winsize", "numerosity", "allposis", "centralposis", "extraposis", "protectzonetype",
                "convexhull", "occupancyarea", "averageeccentricity", "averagespacing", "density"]

all_display_df = pd.DataFrame(columns = column_names)

for n in range(1, run_n + 1):
    print(n)
    base_posis = get_display(full_posi_list, protect_zone_ori = Orientation.Both, radial_weight = radial_weight, tan_weight = tangential_weight)
    extra_posis = get_two_extra_posis(based_posis = base_posis, ori = protect_zone_type)

    my_display = [base_posis, extra_posis]

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

    all_display_df = pd.concat([all_display_df, pd.DataFrame([new_display])], ignore_index=True)


if save_to_csv:
    all_display_df.to_csv("ws%s_%s_angle%s_drctn%s.csv" % (curr_winsize, protect_zone_type, sector_angle, direction), index = False)

if demo_plots:
    savefig = True
    i = 1  # choose the row index you want to plot, it's coln-1
    row = all_display_df.iloc[i]

    base_posis = row['centralposis']
    extra_posis = row['extraposis']
    ka = radial_weight
    kb = tangential_weight

    drawEllipse_full(base_posis, extra_posis, ka=ka, kb=kb, plot_axis_limit_fixed=False, zoomin=True, savefig=savefig)
    drawEllipse_full(base_posis, extra_posis, ka=ka, kb=kb, plot_axis_limit_fixed=False, zoomin=False, savefig=savefig)
    draw_disc_only(base_posis, extra_posis,savefig=savefig)