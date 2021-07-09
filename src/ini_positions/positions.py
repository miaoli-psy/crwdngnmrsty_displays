def generate_all_posis(grid_x = 101, grid_y = 75, linelength = 10):
    '''get full positions in a dimention of grid_x*grid_y'''
    start_x = -0.5*linelength*grid_x + 0.5*linelength
    start_y = -0.5*linelength*grid_y + 0.5*linelength
    positions = []
    for x in range(0, grid_x):
        new_x = start_x + x*linelength
        for y in range(0, grid_y):
            new_y = start_y + y*linelength
            positions.append((new_x, new_y))
    try:
        positions.remove((0,0))#remove the center
    except ValueError:
        pass
    return positions

if __name__ == "__main__":
    debug = True
    if debug == True:
        test_posis = generate_all_posis(grid_x= 11, grid_y= 7, linelength=1)
        print(test_posis)