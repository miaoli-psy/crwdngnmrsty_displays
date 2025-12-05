import os
import pandas as pd

from ellipse import Ellipse, Orientation
from src.process_plane import get_display
from src.draw_displays import drawEllipse_full, draw_disc_only, drawEllipses
from src.displays import generate_display_add_one_extra_discs, get_two_extra_posis

from src.allpositions import AllPositions_full
from src.properties import Properties

curr_winsize = 1
radial_weight = 0.25
tangential_weight = 0.1
protect_zone_type = "radial"
# protect_zone_type = "tangential"

all_posis_Object = AllPositions_full(width = 1920, height = 1080, fovea_radius = 200, window_size = curr_winsize)
full_posi_list = all_posis_Object.generate_all_posi_full(winsize = curr_winsize)
