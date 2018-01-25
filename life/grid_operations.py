import numpy as np
from numba import jit


@jit
def create_random_grid(w, h):
    """Generate random grid"""
    return np.random.randint(0, 2, (w, h), dtype=np.int32)


@jit
def create_empty_grid(w, h):
    """Generate empty grid"""
    return np.zeros((w, h), dtype=np.int32)


@jit
def clear_grid(grid):
    """fill grid with value 0"""
    grid.fill(0)
    # grid[:, :] = 0


@jit
def is_empty(grid):
    """Checxk if grid is empty"""
    return not grid.any()


@jit
def count_neighbours(grid, i, j, h, w):
    """Count live neighbour cells for (i, j) cell """

    i_min = i - 1 if i > 0 else 0
    j_min = j - 1 if j > 0 else 0
    i_max = i + 1 + 1 if i < h - 1 else h
    j_max = j + 1 + 1 if j < w - 1 else w

    neighbours = -grid[i, j]

    # for ii in range(i_min, i_max):
    #     neighbours += np.sum(grid[ii, j_min:j_max])

    for ii in range(i_min, i_max):
        for jj in range(j_min, j_max):
            neighbours += grid[ii, jj]

    # slow
    # neighbours = np.sum(grid[i_min:i_max, j_min:j_max]) - grid[i, j]

    return neighbours


@jit
def update_grid(grid, h, w):
    """Compute next grid following the Conway's rules"""

    if is_empty(grid):
        return grid

    # counting neighbours for every cell
    next_grid = np.zeros((h, w), dtype=np.int32)
    for i in range(h):
        for j in range(w):
            neighbours = count_neighbours(grid, i, j, h, w)

            if (grid[i, j] == 1 and neighbours in (2, 3)) or \
                    (grid[i, j] == 0 and neighbours == 3):
                next_grid[i, j] = 1
            else:
                next_grid[i, j] = 0

    return next_grid


def mouse_to_grid_position(position, cell_size):
    x, y = position
    x_grid = int(x / cell_size)
    y_grid = int(y / cell_size)
    return x_grid, y_grid


def insert_pattern_into_grid(pattern, grid, grid_position):
    (y, x) = pattern.shape
    (m, n) = grid.shape
    if 0 < y <= m and 0 < x <= n:
        grid[grid_position[1]: grid_position[1] + y, grid_position[0]: grid_position[0] + x] = pattern
    else:
        # TODO: give error info
        pass