import math
import warnings
import matplotlib.pyplot as plt
from src.common.process_basic_data_structure import get_diff_between_2_lists
from itertools import combinations


class AllPositions:
    def __init__(self, grid_x=101, grid_y=75, line_length=10, fovea_radius=100):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.line_length = line_length
        self.fovea_radius = fovea_radius
        self.all_posis = self.generate_all_posis()
        self.all_posis_no_fovea = self.get_all_posis_remove_fovea()

    def generate_all_posis(self, width=1920, height=1080):
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
        to_remove = [posi for posi in self.all_posis if
                     math.sqrt((posi[0] ** 2) + (posi[1] ** 2)) < self.fovea_radius]
        return get_diff_between_2_lists(self.all_posis, to_remove)

    def get_all_posi_in_winsize(self, include_fovea=False, winsize=0.8):
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

    def get_all_posi_in_circular(self, radius=400):
        to_remove = [posi for posi in self.all_posis if
                     math.sqrt((posi[0] ** 2) + (posi[1] ** 2)) > radius]
        return get_diff_between_2_lists(self.all_posis, to_remove)


class AllPositions_full:
    def __init__(self, width=1920, height=1080, fovea_radius=100, window_size = 0.6):
        self.width = width
        self.height = height
        self.fovea_radius = fovea_radius
        self.window_size = window_size


    def generate_all_posi_full(self):
        """
        Like generate_all_posis, but for full 1920×1080 grid centered at (0,0),
        using line_length = 1. Coordinates match standard math orientation.
        """

        # center the coordinate system at (0, 0). Transfor grid indices into Cartesian coordinates
        start_x = -0.5 * self.width + 0.5
        start_y = -0.5 * self.height + 0.5

        window_width = int(self.width * self.window_size)
        window_height = int(self.height * self.window_size)

        x_offset = (self.width - window_width) // 2
        y_offset = (self.height - window_height) // 2

        positions = []
        for x in range(x_offset, x_offset + window_width):
            new_x = start_x + x
            for y in range(y_offset, y_offset + window_height):
                new_y = start_y + y
                if math.hypot(new_x, new_y) >= self.fovea_radius and not (new_x == 0 and new_y == 0):
                    positions.append((new_x, new_y))
        return positions

    def generate_posi_in_circle(self, radius = None):

        full_posis = self.generate_all_posi_full()
        max_radius = 0.5 * self.height * self.window_size

        if radius is None:
            radius = max_radius

        elif radius > max_radius:
            warnings.warn(f"Input radius {radius} exceeds maximum effective radius {max_radius:.2f}. Limiting to {max_radius:.2f}.")
            radius = max_radius

        return [(x, y) for (x, y) in full_posis if math.hypot(x, y) <= radius]


    def generate_sector_posi(self, angle_deg=20, direction_deg=0, all_positions=None):
        """
        Returns positions within a sector from (0, 0) with given angle and direction (both in degrees).
        Excludes points within the fovea.
        angle_deg: 扇形夹角
        direction_deg: 3 o'clock 0 deg, 12 o'clock 90 deg
        all_positions: if None, get all possible positions in circular region
        """
        # all_positions = self.generate_all_posi_full()
        if all_positions is None:
            all_positions = self.generate_posi_in_circle(radius=self.height/2)

        # converts sector angle and direction into radians
        angle_rad = math.radians(angle_deg) / 2  # Half on each side
        direction_rad = math.radians(direction_deg) % (
                    2 * math.pi)  # ensure direction_rad is in [0, 2pi]

        sector_positions = []
        for x, y in all_positions:
            # converts Cartesian to polar angle theta(in radians)
            theta = math.atan2(y, x)
            theta = (theta + 2 * math.pi) % (2 * math.pi)

            # calcualte minimal angular difference between point angle and sector direction
            diff = abs(((theta - direction_rad + math.pi) % (2 * math.pi)) - math.pi)
            # if within the sector wedge, keep the point
            if diff <= angle_rad:
                sector_positions.append((x, y))

        return sector_positions


if __name__ == "__main__":
    debug = True
    if debug:
        # test_posis = AllPositions()
        # all = test_posis.all_posis_no_fovea
        # ax = plt.subplot()
        # for posi in all:
        #     ax.plot(posi[0], posi[1], marker=".", markersize=1)
        # ax.set_xlim(-450, 450)
        # ax.set_ylim(-400, 400)
        # ax.set_aspect("equal")
        # plt.show()
        #
        # ax2 = plt.subplot()
        # win06 = test_posis.get_all_posi_in_winsize(winsize=0.6)
        # for posi in win06:
        #     ax2.plot(posi[0], posi[1], marker=".", markersize=1)
        # ax2.set_xlim(-450, 450)
        # ax2.set_ylim(-400, 400)
        # ax2.set_aspect("equal")
        # plt.show()
        #
        # ax3 = plt.subplot()
        # display_circular = test_posis.get_all_posi_in_circular()
        # for posi in display_circular:
        #     ax3.plot(posi[0], posi[1], marker=".", markersize=1)
        # ax3.set_xlim(-450, 450)
        # ax3.set_ylim(-400, 400)
        # ax3.set_aspect("equal")
        # plt.show()
        #
        test_posi_full = AllPositions_full(window_size = 0.8)
        # ax4 = plt.subplot()
        # pixel_posis = test_posi_full.generate_all_posi_full()
        # sampled = pixel_posis[::500]  # 避免卡住，采样一点 每500取一个点
        # for pos in sampled:
        #     ax4.plot(pos[0], pos[1], marker=".", markersize=1)
        # ax4.set_xlim(-960, 960)
        # ax4.set_ylim(-540, 540)
        # ax4.set_aspect('equal')
        # plt.show()
        #
        ax5 = plt.subplot()
        pixel_posis = test_posi_full.generate_sector_posi(angle_deg=90, direction_deg=0)
        sampled = pixel_posis[::50]
        for pos in sampled:
            ax5.plot(pos[0], pos[1], marker=".", markersize=1)
        ax5.set_xlim(-960, 960)
        ax5.set_ylim(-540, 540)
        ax5.set_aspect('equal')
        plt.show()

        posis_gen_test = AllPositions_full(window_size=0.6)
        filter_circuler_posis = posis_gen_test.generate_posi_in_circle(radius=1080)
        ax6 = plt.subplot()
        sampled = filter_circuler_posis[::500]
        for pos in sampled:
            ax6.plot(pos[0], pos[1], marker=".", markersize=1)
        ax6.set_xlim(-960, 960)
        ax6.set_ylim(-540, 540)
        ax6.set_aspect('equal')
        plt.show()


