
import os
from tqdm import tqdm
import pandas as pd
from ellipse import Ellipse, Orientation
from src.process_plane import get_display
from src.draw_displays import drawEllipse_full, draw_disc_only, drawEllipses
from src.displays import get_two_extra_both_ori

from src.allpositions import AllPositions_full
from src.properties import Properties


curr_winsize = 1
sector_angle = 170# 0-360
direction =  0 # 0-360
fovea_radius = 100 # fovea where no disc is allowed
circular_region_radius = 512 # circular region allowed discs
radial_weight = 0.25
tangential_weight = 0.1
save_to_csv = True
savefig = True
demo_plots = False
run_n = 10000

all_posis_Object = AllPositions_full(width = 1920, height = 1080, fovea_radius = 200, window_size = curr_winsize)
filter_circular_posis = all_posis_Object.generate_posi_in_circle(radius = circular_region_radius)

full_posi_list = all_posis_Object.generate_sector_posi(angle_deg = sector_angle,
                                                       direction_deg = direction,
                                                       all_positions = filter_circular_posis)


column_names = ["n", "winsize", "numerosity", "allposis", "centralposis", "extraposis", "protectzonetype",
                "convexhull", "occupancyarea", "averageeccentricity", "averagespacing", "density"]


rows = []
for n in tqdm(range(1, run_n + 1), desc="Generating Displays"):
    base_posis = get_display(full_posi_list, protect_zone_ori=Orientation.Both,
                             radial_weight=radial_weight, tan_weight=tangential_weight)
    extra_posis = get_two_extra_both_ori(based_posis=base_posis,
                                         radial_weight=radial_weight,
                                         tan_weight=tangential_weight)

    my_display = [base_posis, extra_posis]

    properites = Properties(my_display[0] + my_display[1])

    new_display = {"n": n,
                   "winsize": curr_winsize,
                   "numerosity": len(my_display[0]) * 3,
                   "allposis": my_display[0] + my_display[1],
                   "centralposis": my_display[0],
                   "extraposis": my_display[1]}

    rows.append(new_display)

all_display_df = pd.DataFrame(rows, columns=column_names)


if demo_plots:
    i = 96  # choose the row index you want to plot, it's coln-1
    row = all_display_df.iloc[i]

    base_posis = row['centralposis']
    extra_posis = row['extraposis']
    ka = radial_weight
    kb = tangential_weight

    drawEllipse_full(base_posis, extra_posis, ka=ka, kb=kb, plot_axis_limit_fixed=False, zoomin=False, savefig=savefig)
    draw_disc_only(base_posis, extra_posis,savefig=savefig)


if save_to_csv:
    # curr dir
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # file name
    file_name = "ws%s_neutral_angle%s_drctn%s.csv" % (curr_winsize, sector_angle, direction)
    save_path = os.path.join(current_dir, file_name)
    all_display_df.to_csv(save_path, index = False)