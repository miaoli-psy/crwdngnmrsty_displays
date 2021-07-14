import math
import matplotlib.pyplot as plt
from src.common.process_basic_data_structure import get_diff_between_2_lists


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
            positions.remove((0, 0))  # remove the center
        except ValueError:
            pass
        return positions

    def fovea_posis(self):
        return [posi for posi in self.all_posis if math.sqrt((posi[0] ** 2) + (posi[1] ** 2)) < self.fovea_radius]

    def get_all_posis_remove_fovea(self):
        return get_diff_between_2_lists(self.all_posis, self.fovea_posis())


if __name__ == "__main__":
    debug = True
    if debug:
        test_posis = Positions(grid_x = 101, grid_y = 75, line_length = 10, fovea_radius = 100)
        fovea = test_posis.fovea_posis()
        all = test_posis.all_posis_no_fovea
        ax = plt.subplot()
        for posi in all:
            ax.plot(posi[0], posi[1], marker = ".", markersize = 1)