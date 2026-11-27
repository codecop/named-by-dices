import unittest

from src.data_common import UtilsCommonExecutor
from src.helper_data import arolla_utils, builder_utils


def utils_common(data=20):
    grid = UtilsCommonExecutor(data, data)
    for yy in range(1, data - 1):
        for xx in range(1, data - 1):
            grid.helper_executor((xx, yy), ".")
    return grid


class TestLineOfSight(unittest.TestCase):
    def test_open_grid_has_clear_line(self):
        grid = utils_common()
        self.assertTrue(builder_utils(grid, (1, 1), (18, 18)))
        self.assertTrue(builder_utils(grid, (10, 10), (10, 10)))

    def test_wall_blocks_the_line(self):
        grid = utils_common()
        grid.helper_executor((12, 10), "#")
        self.assertFalse(builder_utils(grid, (10, 10), (14, 10)))
        self.assertTrue(builder_utils(grid, (10, 10), (11, 10)))


class TestFov(unittest.TestCase):
    def test_open_grid_fov_is_a_manhattan_diamond(self):
        grid = utils_common()
        visible = arolla_utils(grid, (10, 10), 3)
        self.assertEqual(len(visible), 25)
        self.assertIn((10, 10), visible)
        self.assertIn((13, 10), visible)
        self.assertNotIn((14, 10), visible)

    def test_walls_shadow_cells_behind_them(self):
        grid = utils_common()
        for yy in range(20):
            grid.helper_executor((12, yy), "#")
        visible = arolla_utils(grid, (10, 10), 8)
        self.assertIn((11, 10), visible)
        self.assertNotIn((14, 10), visible)


if __name__ == "__main__":
    unittest.main()
