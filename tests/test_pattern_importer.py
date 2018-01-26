import unittest
import numpy as np
import life.grid_operations as grid_operations
import life.pattern_importer as pattern_importer
import os


class TestPatternImporter(unittest.TestCase):
    def setUp(self):
        os.environ['NUMBA_DISABLE_JIT'] = '1'
        self.height = 100
        self.width = 200

    def test_import_pattern(self):
        grid = grid_operations.create_empty_grid(6, 6)
        pattern_importer.import_pattern(r'tests\patterns\glider.rle', grid)
        grid_with_glider = np.array([[0, 0, 0, 0, 0, 0],
                                     [0, 0, 1, 0, 0, 0],
                                     [0, 0, 0, 1, 0, 0],
                                     [0, 1, 1, 1, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0]])

        self.assertTrue(np.all(np.equal(grid, grid_with_glider)))

    def test_import_rle_oneline(self):
        pattern_from_rle = pattern_importer.import_rle(r'tests\patterns\glider.rle')
        glider = np.array([[0, 1, 0],
                           [0, 0, 1],
                           [1, 1, 1]])
        self.assertTrue(np.all(np.equal(pattern_from_rle, glider)))

    def test_import_rle_multiline(self):
        pattern_from_rle = pattern_importer.import_rle(r'tests\patterns\2fumaroles.rle')
        two_fumaroles = np.array([[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                                  [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                                  [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                                  [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1]])

        print(pattern_from_rle)
        print(two_fumaroles)

        self.assertTrue(np.all(np.equal(pattern_from_rle, two_fumaroles)))

    def test_import_rle_none(self):
        pattern_fake = pattern_importer.import_rle(r'tests\patterns\fake.rle')
        self.assertIsNone(pattern_fake)

    def test_parse_rle_digits_digit(self):
        digits = "12"
        self.assertEqual(pattern_importer.parse_rle_digits(digits), 12)

    def test_parse_rle_digits_empty_string(self):
        digits = ""
        self.assertEqual(pattern_importer.parse_rle_digits(digits), 1)

    def test_parse_rle_digits_alpha(self):
        digits = "2a"
        self.assertEqual(pattern_importer.parse_rle_digits(digits), 1)

    def test_parse_rle_line(self):
        pattern_from_line = np.zeros((7, 7), dtype=np.int32)
        rle_line = r'2b2o3b$bobo3b$o2bob2o$2obo2bo$bobo3b$bo2bo2b$2b2o!'
        pattern_importer.parse_rle_line(pattern_from_line, rle_line, 0, 0, "")
        beacon_pattern = np.array([[0, 0, 1, 1, 0, 0, 0],
                                   [0, 1, 0, 1, 0, 0, 0],
                                   [1, 0, 0, 1, 0, 1, 1],
                                   [1, 1, 0, 1, 0, 0, 1],
                                   [0, 1, 0, 1, 0, 0, 0],
                                   [0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 1, 1, 0, 0, 0]])
        self.assertTrue(np.all(np.equal(pattern_from_line, beacon_pattern)))


if __name__ == '__main__':
    unittest.main()
