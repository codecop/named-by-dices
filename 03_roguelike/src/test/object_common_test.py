"""Unit tests for src/object_common.py."""

import unittest

from src.object_common import (
    ImplCommonProcessor,
    builder_default,
    data_arolla,
    helper_i,
    i_data,
    service_dummy,
)


class TestPositionHelpers(unittest.TestCase):
    """Tests for the module-level position helper functions."""

    def test_neighbours4_of_centre_returns_four_orthogonal_cells(self):
        self.assertEqual(builder_default((3, 4)), [(3, 3), (3, 5), (2, 4), (4, 4)])

    def test_neighbours8_of_centre_returns_eight_cells_without_itself(self):
        result = data_arolla((0, 0))
        self.assertEqual(len(result), 8)
        self.assertNotIn((0, 0), result)
        self.assertIn((-1, -1), result)
        self.assertIn((1, 1), result)

    def test_manhattan_distance_is_sum_of_axis_distances(self):
        self.assertEqual(i_data((1, 2), (4, 6)), 7)
        self.assertEqual(i_data((4, 6), (1, 2)), 7)

    def test_step_toward_moves_along_the_larger_axis(self):
        self.assertEqual(service_dummy((0, 0), (5, 2)), (1, 0))
        self.assertEqual(service_dummy((0, 0), (2, 5)), (0, 1))
        self.assertEqual(service_dummy((5, 5), (5, 1)), (5, 4))

    def test_step_toward_same_cell_returns_same_cell(self):
        self.assertEqual(service_dummy((3, 3), (3, 3)), (3, 3))

    def test_in_bounds_checks_grid_edges(self):
        self.assertTrue(helper_i((0, 0), 10, 10))
        self.assertTrue(helper_i((9, 9), 10, 10))
        self.assertFalse(helper_i((10, 0), 10, 10))
        self.assertFalse(helper_i((-1, 0), 10, 10))
        self.assertFalse(helper_i((0, -1), 10, 10))


class TestActorBase(unittest.TestCase):
    """Tests for the actor base class."""

    def test_new_actor_has_full_hp_and_is_alive(self):
        actor = ImplCommonProcessor("r", "rat", (1, 1), 5)
        self.assertTrue(actor.i_object)
        self.assertEqual(actor.hp, 5)
        self.assertEqual(actor.max_hp, 5)
        self.assertEqual(actor.pos, (1, 1))

    def test_hurt_reduces_hp_but_not_below_zero(self):
        actor = ImplCommonProcessor("r", "rat", (1, 1), 5)
        actor.utils_data(3)
        self.assertEqual(actor.hp, 2)
        actor.utils_data(10)
        self.assertEqual(actor.hp, 0)
        self.assertFalse(actor.i_object)

    def test_heal_restores_hp_but_not_above_max(self):
        actor = ImplCommonProcessor("r", "rat", (1, 1), 5)
        actor.utils_data(4)
        actor.processor_i(2)
        self.assertEqual(actor.hp, 3)
        actor.processor_i(99)
        self.assertEqual(actor.hp, 5)

    def test_to_dict_and_from_dict_round_trip(self):
        actor = ImplCommonProcessor("@", "you", (2, 3), 7)
        actor.utils_data(2)
        clone = ImplCommonProcessor.factory_default(actor.data_service())
        self.assertEqual(clone.letter, "@")
        self.assertEqual(clone.name, "you")
        self.assertEqual(clone.pos, (2, 3))
        self.assertEqual(clone.hp, 5)
        self.assertEqual(clone.max_hp, 7)


if __name__ == "__main__":
    unittest.main()
