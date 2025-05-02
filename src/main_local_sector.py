import os
import random
from tqdm import tqdm
import pandas as pd
from ellipse import Ellipse, Orientation
from src.process_plane import get_display
from src.draw_displays import drawEllipse_full, draw_disc_only, drawEllipses
from src.displays import generate_display_add_one_extra_discs, get_two_extra_posis

from src.allpositions import AllPositions_full
from src.properties import Properties


curr_winsize = 1
sector_angle = 170 # 0-360
direction =  0 # 0-360
fovea_radius = 100 # fovea where no disc is allowed
circular_region_radius = 512 # circular region allowed discs
radial_weight = 0.25
tangential_weight = 0.1
protect_zone_type = "radial"
# protect_zone_type = "tangential"
save_to_csv = True
savefig = False
demo_plots = False
run_n = 50000
write_full_properites = False

all_posis_Object = AllPositions_full(width = 1920, height = 1080, fovea_radius = 200, window_size = curr_winsize)
filter_circular_posis = all_posis_Object.generate_posi_in_circle(radius = circular_region_radius)

full_posi_list = all_posis_Object.generate_sector_posi(angle_deg = sector_angle, direction_deg = direction, all_positions = filter_circular_posis)


column_names = ["n", "winsize", "numerosity", "allposis", "centralposis", "extraposis", "protectzonetype",
                "convexhull", "occupancyarea", "averageeccentricity", "averagespacing", "density"]

# all_display_df = pd.DataFrame(columns = column_names)

rows = []
for n in tqdm(range(1, run_n + 1), desc="Generating Displays"): # 加入进度条
    # print(n)
    base_posis = get_display(full_posi_list, protect_zone_ori = Orientation.Both, radial_weight = radial_weight, tan_weight = tangential_weight)
    extra_posis = get_two_extra_posis(based_posis = base_posis, ori = protect_zone_type)

    my_display = [base_posis, extra_posis]

    properites = Properties(my_display[0] + my_display[1])

    if write_full_properites:

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
    else:
        new_display = {"n":                   n,
                       "winsize":             curr_winsize,
                       "numerosity":          len(my_display[0]) * 3,
                       "allposis":            my_display[0] + my_display[1],
                       "centralposis":        my_display[0],
                       "extraposis":          my_display[1],
                       "protectzonetype":     protect_zone_type}

    rows.append(new_display)

# all_display_df = pd.concat([all_display_df, pd.DataFrame([new_display])], ignore_index=True)
all_display_df = pd.DataFrame(rows, columns=column_names)


if save_to_csv:
    # curr dir
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # file name
    file_name = "ws%s_%s_angle%s_drctn%s.csv" % (curr_winsize, protect_zone_type, sector_angle, direction)
    save_path = os.path.join(current_dir, file_name)
    all_display_df.to_csv(save_path, index = False)

if demo_plots:

    i = 0  # choose the row index you want to plot, it's coln-1
    row = all_display_df.iloc[i]

    base_posis = row['centralposis']
    extra_posis = row['extraposis']
    ka = radial_weight
    kb = tangential_weight

    drawEllipse_full(base_posis, extra_posis, ka=ka, kb=kb, plot_axis_limit_fixed=False, zoomin=True, savefig=savefig)
    drawEllipse_full(base_posis, extra_posis, ka=ka, kb=kb, plot_axis_limit_fixed=False, zoomin=False, savefig=savefig)
    draw_disc_only(base_posis, extra_posis,savefig=savefig)