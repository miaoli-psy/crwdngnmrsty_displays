import os
import pandas as pd
from tqdm import tqdm

from ellipse import Ellipse, Orientation
from src.process_plane import get_display
from src.draw_displays import drawEllipse_full, draw_disc_only, drawEllipses
from src.displays import generate_display_add_one_extra_discs, get_two_extra_posis

from src.allpositions import AllPositions_full
from src.properties import Properties

curr_winsize = 1
radial_weight = 0.55
tangential_weight = 0.22
protect_zone_type = "radial"
protect_zone_type = "tangential"

demo_plots = True
savefig = True

all_posis_Object = AllPositions_full(width = 1920, height = 1080, fovea_radius = 200, window_size = curr_winsize)
full_posi_list = all_posis_Object.generate_all_posi_full()

run_n = 2

column_names = ["n", "winsize", "numerosity", "allposis", "centralposis", "extraposis", "protectzonetype",
                "convexhull", "occupancyarea", "averageeccentricity", "averagespacing", "density"]


rows = []
for n in tqdm(range(1, run_n + 1), desc="Generating Displays"):
    base_posis = get_display(full_posi_list, protect_zone_ori=Orientation.Both,
                             radial_weight=radial_weight, tan_weight=tangential_weight)
    extra_posis = get_two_extra_posis(based_posis=base_posis, ori=protect_zone_type,
                                      radial_weight=radial_weight, tan_weight=tangential_weight)

    my_display = [base_posis, extra_posis]

    properites = Properties(my_display[0] + my_display[1])

    new_display = {"n": n,
                   "winsize": curr_winsize,
                   "numerosity": len(my_display[0]) * 3,
                   "allposis": my_display[0] + my_display[1],
                   "centralposis": my_display[0],
                   "extraposis": my_display[1],
                   "protectzonetype": protect_zone_type}

    rows.append(new_display)

all_display_df = pd.DataFrame(rows, columns=column_names)



if demo_plots:
    i = 1  # choose the row index you want to plot, it's coln-1
    row = all_display_df.iloc[i]

    base_posis = row['centralposis']
    extra_posis = row['extraposis']
    ka = radial_weight
    kb = tangential_weight

    drawEllipse_full(base_posis, extra_posis, ka=ka, kb=kb, plot_axis_limit_fixed=False, zoomin=False, savefig=savefig)
    draw_disc_only(base_posis, extra_posis,savefig=savefig)