import math
import matplotlib.pyplot as plt
from src.common.process_basic_data_structure import get_diff_between_2_lists
from itertools import combinations


class Positions:
    def __init__(self, grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.line_length = line_length
        self.fovea_radius = fovea_radius
        self.all_posis = self.generate_all_posis()
        self.all_posis_no_fovea = self.get_all_posis_remove_fovea()

    def generate_all_posis(self):
        """get full positions in a dimension of grid_x*grid_y"""
        start_x = -0.5 * self.line_length * self.grid_x + 0.5 * self.line_length
        start_y = -0.5 * self.line_length * self.grid_y + 0.5 * self.line_length
        positions = []
        for x in range(0, self.grid_x):
            new_x = start_x + x * self.line_length
            for y in range(0, self.grid_y):
                new_y = start_y + y * self.line_length
                positions.append((new_x, new_y))
        try:
            positions.remove((0, 0))
        except ValueError:
            pass
        return positions

    def get_all_posis_remove_fovea(self):
        to_remove = [posi for posi in self.all_posis if math.sqrt((posi[0] ** 2) + (posi[1] ** 2)) < self.fovea_radius]
        return get_diff_between_2_lists(self.all_posis, to_remove)

    def get_all_posi_in_winsize(self, include_fovea = False, winsize = 0.8):
        max_corrdinate = max(self.all_posis_no_fovea)
        outer_posi_list = list()
        if include_fovea:
            all_posi_list = self.all_posis
        else:
            all_posi_list = self.all_posis_no_fovea
        # TODO optimize
        for posi in all_posi_list:
            if abs(posi[0]) > max_corrdinate[0] * winsize or abs(posi[1]) > max_corrdinate[1] * winsize:
                outer_posi_list.append(posi)

        return get_diff_between_2_lists(all_posi_list, outer_posi_list)


if __name__ == "__main__":
    debug = True
    if debug:
        test_posis = Positions()
        all = test_posis.all_posis_no_fovea
        ax = plt.subplot()
        for posi in all:
            ax.plot(posi[0], posi[1], marker = ".", markersize = 1)
            ax.set_xlim(-450, 450)
            ax.set_ylim(-400, 400)
        plt.show()
        ax2 = plt.subplot()
        win06 = test_posis.get_all_posi_in_winsize(winsize = 0.6)
        for posi in win06:
            ax2.plot(posi[0], posi[1], marker = ".", markersize = 1)
            ax2.set_xlim(-450, 450)
            ax2.set_ylim(-400, 400)
        plt.show()