from life.rle_importer import import_rle


def import_pattern(pattern_file, grid, grid_position=(1, 1)):
    pattern = import_rle(pattern_file)
    insert_pattern_into_grid(pattern, grid, grid_position)


def insert_pattern_into_grid(pattern, grid, grid_position):
    (y, x) = pattern.shape
    (m, n) = grid.shape
    if y <= m and x <= n:
        grid[grid_position[1]: grid_position[1] + y, grid_position[0]: grid_position[0] + x] = pattern
    else:
        # TODO: give error info
        pass