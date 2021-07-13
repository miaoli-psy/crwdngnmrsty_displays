import math

from src.common.process_basic_data_structure import get_diff_between_2_lists


def generate_all_posis(grid_x = 101, grid_y = 75, linelength = 10):
    '''get full positions in a dimention of grid_x*grid_y'''
    start_x = -0.5 * linelength * grid_x + 0.5 * linelength
    start_y = -0.5 * linelength * grid_y + 0.5 * linelength
    positions = []
    for x in range(0, grid_x):
        new_x = start_x + x * linelength
        for y in range(0, grid_y):
            new_y = start_y + y * linelength
            positions.append((new_x, new_y))
    try:
        positions.remove((0, 0))  # remove the center
    except ValueError:
        pass
    return positions


def get_fovea_posis(posilist, r = 100):
    return [posi for posi in posilist if math.sqrt((posi[0] ** 2) + (posi[1] ** 2)) < r]


def remove_fovea_posis(r = 100, grid_x = 101, grid_y = 75, linelength = 10):
    # initial positions
    posis = generate_all_posis(grid_x = grid_x, grid_y = grid_y, linelength = linelength)
    # fovia posis
    fovea_posis = get_fovea_posis(posilist = posis, r = r)
    return get_diff_between_2_lists(posis, fovea_posis)


if __name__ == "__main__":
    debug = True
    if debug:
        test_posis = generate_all_posis(grid_x = 10, grid_y = 7, linelength = 1)
        left = remove_fovea_posis()