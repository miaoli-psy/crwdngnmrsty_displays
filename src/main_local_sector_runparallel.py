import os
import random
from tqdm import tqdm
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from ellipse import Orientation
from src.process_plane import get_display
from src.displays import get_two_extra_posis
from src.allpositions import AllPositions_full
from src.properties import Properties

# Fixed parameters
n_cores = 36
curr_winsize = 1
sector_angle = 120
direction = 0
fovea_radius = 100
circular_region_radius = 512
radial_weight = 0.25
tangential_weight = 0.1
# protect_zone_type = "radial"
protect_zone_type = "tangential"
save_to_csv = True
demo_plots = False
savefig = False
run_n = 100000
write_full_properites = False

# Generate possible positions once, outside parallel loop
all_posis_Object = AllPositions_full(width=1920, height=1080, fovea_radius=200, window_size=curr_winsize)
filter_circular_posis = all_posis_Object.generate_posi_in_circle(radius=circular_region_radius)
full_posi_list = all_posis_Object.generate_sector_posi(angle_deg=sector_angle, direction_deg=direction, all_positions=filter_circular_posis)


# The worker function
def generate_one_display(n):
    base_posis = get_display(full_posi_list, protect_zone_ori=Orientation.Both, radial_weight=radial_weight, tan_weight=tangential_weight)
    extra_posis = get_two_extra_posis(based_posis=base_posis, ori=protect_zone_type)
    my_display = [base_posis, extra_posis]

    if write_full_properites:
        props = Properties(my_display[0] + my_display[1])
        return {
            "n": n,
            "winsize": curr_winsize,
            "numerosity": len(my_display[0]) * 3,
            "allposis": my_display[0] + my_display[1],
            "centralposis": my_display[0],
            "extraposis": my_display[1],
            "protectzonetype": protect_zone_type,
            "convexhull": props.convexhull,
            "occupancyarea": props.occupancy_area,
            "averageeccentricity": props.averge_eccentricity,
            "averagespacing": props.average_spacing,
            "density": props.density
        }
    else:
        return {
            "n": n,
            "winsize": curr_winsize,
            "numerosity": len(my_display[0]) * 3,
            "allposis": my_display[0] + my_display[1],
            "centralposis": my_display[0],
            "extraposis": my_display[1],
            "protectzonetype": protect_zone_type
        }


# Parallel execution
if __name__ == "__main__":
    column_names = ["n", "winsize", "numerosity", "allposis", "centralposis", "extraposis", "protectzonetype"]
    if write_full_properites:
        column_names += ["convexhull", "occupancyarea", "averageeccentricity", "averagespacing", "density"]

    with ProcessPoolExecutor(max_workers = n_cores) as executor:
        results = list(tqdm(executor.map(generate_one_display, range(1, run_n + 1)), total=run_n))

    all_display_df = pd.DataFrame(results, columns=column_names)

    if save_to_csv:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = "ws%s_%s_angle%s_drctn%s.csv" % (curr_winsize, protect_zone_type, sector_angle, direction)
        save_path = os.path.join(current_dir, file_name)
        all_display_df.to_csv(save_path, index=False)

# print("Using", os.cpu_count(), "cores")