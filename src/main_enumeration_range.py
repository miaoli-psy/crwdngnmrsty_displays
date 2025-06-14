import os
import random
from tqdm import tqdm
import pandas as pd

from ellipse import Ellipse, Orientation
from src.process_plane import get_display
from src.draw_displays import drawEllipse_full, draw_disc_only
from src.displays import get_two_extra_posis
from src.allpositions import AllPositions_full

# === Configuration ===
curr_winsize = 1
sector_angle = 5
direction = 0
fovea_radius = 100
circular_region_radius = 512
radial_weight = 0.25
tangential_weight = 0.1
protect_zone_type = "radial"
# protect_zone_type = "tangential"
save_to_csv = False
savefig = False
demo_plots = True
run_n = 1000

# === Generate all allowed positions ===
all_posis_Object = AllPositions_full(
    width=1920,
    height=1080,
    fovea_radius=200,
    window_size=curr_winsize
)
filter_circular_posis = all_posis_Object.generate_posi_in_circle(radius=circular_region_radius)
full_posi_list = all_posis_Object.generate_sector_posi(
    angle_deg=sector_angle,
    direction_deg=direction,
    all_positions=filter_circular_posis
)

# === Main loop to generate displays ===
rows = []

for n in tqdm(range(1, run_n + 1), desc="Generating Displays"):
    base_posis = get_display(
        full_posi_list,
        protect_zone_ori=Orientation.Both,
        radial_weight=radial_weight,
        tan_weight=tangential_weight
    )

    extra_posis = get_two_extra_posis(based_posis=base_posis, ori=protect_zone_type)

    if len(base_posis) > 3:
        continue  # limit to 3 central discs

    expected_extras = len(base_posis) * 2
    if len(extra_posis) != expected_extras:
        continue  # enforce consistency

    new_display = {
        "n": n,
        "winsize": curr_winsize,
        "numerosity": len(base_posis) * 3,
        "protectzonetype": protect_zone_type,
        "centralposis": base_posis,
        "extraposis": extra_posis
    }

    # Assign centerN and extraN with strict list structure
    for i in range(3):
        if i < len(base_posis):
            center = [base_posis[i]]
            extra = [extra_posis[i * 2], extra_posis[i * 2 + 1]]
            new_display[f"center{i + 1}"] = center
            new_display[f"extra{i + 1}"] = extra
        else:
            center = None
            extra = None
            new_display[f"center{i + 1}"] = None
            new_display[f"extra{i + 1}"] = None

        # Add combined n3_posis_* if applicable
        if i == 0:
            new_display["n3_posis_close"] = center + extra if center and extra else None
        if i == 1:
            new_display["n3_posis_far"] = center + extra if center and extra else None

    # Add n4_posis_close and n4_posis_far based on n3_posis_* if both exist
    if new_display["n3_posis_close"] is not None and new_display["n3_posis_far"] is not None:
        new_display["n4_posis_close"] = new_display["n3_posis_close"] + [random.choice(new_display["n3_posis_far"])]
        new_display["n4_posis_far"] = new_display["n3_posis_far"] + [random.choice(new_display["n3_posis_close"])]
    else:
        new_display["n4_posis_close"] = None
        new_display["n4_posis_far"] = None

    # Add n4_posis_both from center1 + center2 + 1 from extra1 + 1 from extra2
    if (new_display["center1"] is not None and
            new_display["center2"] is not None and
            new_display["extra1"] is not None and
            new_display["extra2"] is not None
    ):
        n4_posis_both = (
                new_display["center1"] +
                new_display["center2"] +
                [random.choice(new_display["extra1"])] +
                [random.choice(new_display["extra2"])]
        )
        new_display["n4_posis_both"] = n4_posis_both
    else:
        new_display["n4_posis_both"] = None


    # Add n5_posis_close and n5_posis_far
    if (
        new_display["n3_posis_close"] is not None and
        new_display["center2"] is not None and
        new_display["extra2"] is not None
    ):
        new_display["n5_posis_close"] = new_display["n3_posis_close"] + new_display["center2"] + [random.choice(new_display["extra2"])]
    else:
        new_display["n5_posis_close"] = None

    if (
        new_display["n3_posis_far"] is not None and
        new_display["center1"] is not None and
        new_display["extra1"] is not None
    ):
        new_display["n5_posis_far"] = new_display["n3_posis_far"] + new_display["center1"] + [random.choice(new_display["extra1"])]
    else:
        new_display["n5_posis_far"] = None

    rows.append(new_display)


# === Build DataFrame ===
all_display_df = pd.DataFrame(rows)

# === Save to CSV ===
if save_to_csv:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f"ws{curr_winsize}_{protect_zone_type}_angle{sector_angle}_drctn{direction}.csv"
    save_path = os.path.join(current_dir, file_name)
    all_display_df.to_csv(save_path, index=False)
    print(f"Saved to: {save_path}")

# === Optional plotting ===
if demo_plots:
    i = 0  # index of row to visualize
    row = all_display_df.iloc[i]
    base_posis = row['centralposis']
    extra_posis = row['extraposis']
    ka = radial_weight
    kb = tangential_weight

    drawEllipse_full(base_posis, extra_posis, ka=ka, kb=kb, plot_axis_limit_fixed=False, zoomin=True, savefig=savefig)
    drawEllipse_full(base_posis, extra_posis, ka=ka, kb=kb, plot_axis_limit_fixed=False, zoomin=False, savefig=savefig)
    draw_disc_only(base_posis, extra_posis, savefig=savefig)
