import pandas as pd
import numpy as np


if __name__ == '__main__':
    write_to_excel = False
    PATH = "../../selected_display/"
    FILE = "ms2_displays_triplets.xlsx"

    # read display file
    displays = pd.read_excel(PATH + FILE)

    table = pd.pivot_table(displays,
                           index = ["protectzonetype", "winsize"],
                           values = ["convexhull",
                                     "occupancyarea_no_fovea",
                                     "density_no_fovea",
                                     "occupancyarea",
                                     "averageeccentricity",
                                     "averagespacing"],
                           aggfunc = {"convexhull": [np.mean, np.std],
                                      "occupancyarea_no_fovea": [np.mean, np.std],
                                      "occupancyarea": [np.mean, np.std],
                                      "density_no_fovea": [np.mean, np.std],
                                      "averagespacing": [np.mean, np.std],
                                      "averageeccentricity": [np.mean, np.std]})
    if write_to_excel:
        table.to_excel("pt.xlsx")
