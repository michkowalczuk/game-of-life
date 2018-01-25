import unittest
import numpy as np
import life.grid_operations as grid_operations
import os


class TestGridOperations(unittest.TestCase):
    def setUp(self):
        os.environ['NUMBA_DISABLE_JIT'] = '1'
        self.height = 100
        self.width = 200

    def test_create_random_grid_shape(self):
        random_grid = grid_operations.create_random_grid(self.height, self.width)
        self.assertEqual(random_grid.shape, (self.height, self.width))

    def test_create_random_grid_values(self):
        random_grid = grid_operations.create_random_grid(self.height, self.width)
        self.assertTrue((np.all(0 <= random_grid) and np.all(random_grid <= 1)))

    def test_create_empty_grid_shape(self):
        clear_grid = grid_operations.create_empty_grid(self.height, self.width)
        self.assertEqual(clear_grid.shape, (self.height, self.width))

    def test_create_empty_grid_value(self):
        empty_grid = grid_operations.create_empty_grid(self.height, self.width)
        self.assertTrue(np.all(empty_grid == 0))

    def test_clear_grid(self):
        test_grid = np.ones((self.height, self.width), dtype=np.int32)
        grid_operations.clear_grid(test_grid)
        self.assertTrue(np.all(test_grid == 0))

    def test_is_empty(self):
        test_grid = np.zeros((self.height, self.width), dtype=np.int32)
        self.assertTrue(grid_operations.is_empty(test_grid))

    def test_count_neighbours_zeros(self):
        test_grid = np.zeros((self.height, self.width), dtype=np.int32)
        neighbours = grid_operations.count_neighbours(test_grid,
                                                      self.height // 2,
                                                      self.width // 2,
                                                      self.height,
                                                      self.width)
        self.assertEqual(neighbours, 0)

    def test_count_neighbours_ones(self):
        test_grid = np.ones((self.height, self.width), dtype=np.int32)
        neighbours = grid_operations.count_neighbours(test_grid,
                                                      self.height // 2,
                                                      self.width // 2,
                                                      self.height,
                                                      self.width)
        self.assertEqual(neighbours, 8)

    def test_update_grid_still_lifes(self):
        # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#/media/File:Game_of_life_block_with_border.svg
        block = np.array([[0, 0, 0, 0],
                          [0, 1, 1, 0],
                          [0, 1, 1, 0],
                          [0, 0, 0, 0]])

        self.assertTrue(np.all(np.equal(block, grid_operations.update_grid(block, block.shape[0], block.shape[1]))))

    def test_update_grid_oscillators(self):
        # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#/media/File:Game_of_life_blinker.gif
        blinker_1 = np.array([[0, 0, 0, 0, 0],
                              [0, 0, 1, 0, 0],
                              [0, 0, 1, 0, 0],
                              [0, 0, 1, 0, 0],
                              [0, 0, 0, 0, 0]])

        blinker_2 = np.array([[0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0],
                              [0, 1, 1, 1, 0],
                              [0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0]])

        self.assertTrue(np.all(np.equal(blinker_2, grid_operations.update_grid(blinker_1,
                                                                               blinker_1.shape[0],
                                                                               blinker_1.shape[1]))))

    def test_update_grid_spaceships(self):
        # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#/media/File:Game_of_life_animated_glider.gif
        glider_speed = 4
        glider_1 = np.array([[0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0],
                             [0, 1, 1, 1, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0]])

        glider_5 = np.array([[0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, 1, 0],
                             [0, 0, 1, 1, 1, 0],
                             [0, 0, 0, 0, 0, 0]])
        next_grid = glider_1
        for i in range(glider_speed):
            next_grid = grid_operations.update_grid(next_grid, glider_1.shape[0], glider_1.shape[1])
        self.assertTrue(np.all(np.equal(glider_5, next_grid)))

    def mouse_to_grid_position(self):
        x, y = 3, 24
        cell_size = 10
        x_grid, y_grid = grid_operations.mouse_to_grid_position((x, y), cell_size)
        self.assertEqual((x_grid, y_grid), (0, 2))

    def test_insert_pattern_into_grid(self):
        test_grid = grid_operations.create_empty_grid(5, 5)
        test_pattern = np.ones((3, 3), dtype=np.int32)
        grid_operations.insert_pattern_into_grid(test_pattern, test_grid, (1, 1))
        out_grid = np.array([[0, 0, 0, 0, 0],
                             [0, 1, 1, 1, 0],
                             [0, 1, 1, 1, 0],
                             [0, 1, 1, 1, 0],
                             [0, 0, 0, 0, 0]])
        self.assertTrue(np.all(np.equal(test_grid, out_grid)))


if __name__ == '__main__':
    unittest.main()
