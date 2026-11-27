"""Unit tests for src/data_common.py."""

import random
import unittest

from src.data_common import (
    DUMMY_MANAGER,
    EXECUTOR_AROLLA,
    ArollaImplData,
    ImplProcessorDefault,
    ManagerBusinessArolla,
    ServiceObjectCommon,
    UtilsCommonExecutor,
    data_service,
)
from src.object_common import builder_default


def processor_service(level, start):
    """Flood fill all walkable cells reachable from start (test helper)."""
    seen = {start}
    queue = [start]
    while queue:
        cell = queue.pop()
        for neighbour in builder_default(cell):
            if neighbour not in seen and level.impl_dummy(neighbour):
                seen.add(neighbour)
                queue.append(neighbour)
    return seen


class TestRoom(unittest.TestCase):
    """Tests for the room value object."""

    def test_centre_is_middle_of_rectangle(self):
        room = ArollaImplData(2, 3, 6, 4)
        self.assertEqual(room.utils_common, (5, 5))

    def test_overlaps_detects_touching_inside_and_separated_rooms(self):
        room = ArollaImplData(2, 2, 4, 4)
        self.assertTrue(room.impl_builder(ArollaImplData(6, 2, 4, 4)))
        self.assertTrue(room.impl_builder(ArollaImplData(3, 3, 4, 4)))
        self.assertFalse(room.impl_builder(ArollaImplData(8, 2, 4, 4)))
        self.assertFalse(room.impl_builder(ArollaImplData(2, 8, 4, 4)))

    def test_contains_checks_rectangle_bounds(self):
        room = ArollaImplData(2, 2, 4, 4)
        self.assertTrue(room.object_default((2, 2)))
        self.assertTrue(room.object_default((5, 5)))
        self.assertFalse(room.object_default((6, 2)))
        self.assertFalse(room.object_default((1, 1)))

    def test_random_cell_is_always_interior(self):
        room = ArollaImplData(2, 2, 5, 4)
        rng = random.Random(1)
        for _ in range(50):
            cell = room.processor_factory(rng)
            self.assertTrue(3 <= cell[0] <= 5)
            self.assertTrue(3 <= cell[1] <= 4)

    def test_border_cells_count_matches_perimeter(self):
        room = ArollaImplData(0, 0, 4, 3)
        self.assertEqual(len(room.service_dummy()), 2 * 4 + 2 * 3 - 4)
        self.assertIn((0, 0), room.service_dummy())
        self.assertNotIn((1, 1), room.service_dummy())

    def test_to_dict_and_from_dict_round_trip(self):
        room = ArollaImplData(3, 4, 7, 5)
        clone = ArollaImplData.data_arolla(room.manager_object())
        self.assertEqual(clone.manager_object(), room.manager_object())


class TestTrap(unittest.TestCase):
    """Tests for the trap type."""

    def test_kinds_are_dart_teleport_and_alarm(self):
        self.assertEqual(
            set(ImplProcessorDefault.FACTORY_DEFAULT), {"dart", "teleport", "alarm"}
        )

    def test_hidden_by_default_and_round_trips(self):
        trap = ImplProcessorDefault("dart")
        self.assertFalse(trap.found)
        clone = ImplProcessorDefault.i_utils(trap.object_factory())
        self.assertEqual(clone.kind, "dart")
        self.assertFalse(clone.found)
        trap.found = True
        clone = ImplProcessorDefault.i_utils(trap.object_factory())
        self.assertTrue(clone.found)


class TestGrid(unittest.TestCase):
    """Tests for the tile grid class."""

    def test_out_of_bounds_behaves_like_wall(self):
        grid = UtilsCommonExecutor(10, 10)
        self.assertTrue(grid.factory_default((-1, 0)))
        self.assertTrue(grid.factory_default((0, 10)))
        self.assertFalse(grid.i_business((10, 0)))
        self.assertEqual(grid.utils_data((-1, 0)), "#")

    def test_set_and_get_tile_round_trip(self):
        grid = UtilsCommonExecutor(10, 10)
        grid.helper_executor((3, 4), ".")
        self.assertEqual(grid.utils_data((3, 4)), ".")
        self.assertFalse(grid.factory_default((3, 4)))
        self.assertTrue(grid.impl_dummy((3, 4)))
        self.assertTrue(grid.factory_default((3, 5)))
        self.assertFalse(grid.impl_dummy((3, 5)))

    def test_to_dict_and_from_dict_round_trip(self):
        grid = UtilsCommonExecutor(6, 5)
        grid.helper_executor((2, 2), ">")
        clone = UtilsCommonExecutor.dummy_manager(grid.executor_arolla())
        self.assertEqual(clone.executor_arolla(), grid.executor_arolla())


class TestEntityLayer(unittest.TestCase):
    """Tests for the entity layer of a level."""

    def test_random_free_cell_is_walkable_and_avoids_given_cells(self):
        grid = UtilsCommonExecutor(20, 20)
        for yy in range(1, 19):
            for xx in range(1, 19):
                grid.helper_executor((xx, yy), ".")
        layer = ServiceObjectCommon()
        rng = random.Random(5)
        for _ in range(20):
            cell = layer.business_arolla(grid, rng, avoid=((5, 5),), fallback=(1, 1))
            self.assertTrue(grid.impl_dummy(cell))
            self.assertNotEqual(cell, (5, 5))

    def test_random_free_cell_skips_occupied_cells(self):
        grid = UtilsCommonExecutor(6, 6)
        for yy in range(1, 5):
            for xx in range(1, 5):
                grid.helper_executor((xx, yy), ".")
        layer = ServiceObjectCommon()
        layer.items[(2, 2)] = object()
        layer.monsters[(3, 3)] = object()
        rng = random.Random(2)
        for _ in range(20):
            cell = layer.business_arolla(grid, rng, fallback=(1, 1))
            self.assertNotIn(cell, ((2, 2), (3, 3)))

    def test_random_free_cell_falls_back_when_no_cell_is_free(self):
        grid = UtilsCommonExecutor(4, 4)
        layer = ServiceObjectCommon()
        cell = layer.business_arolla(grid, random.Random(1), fallback=(1, 1))
        self.assertEqual(cell, (1, 1))

    def test_to_dict_and_from_dict_round_trip(self):
        layer = ServiceObjectCommon()
        layer.traps[(2, 3)] = ImplProcessorDefault("alarm", found=True)
        layer.explored.add((1, 1))
        clone = ServiceObjectCommon.dummy_manager(layer.executor_arolla())
        self.assertEqual(clone.executor_arolla(), layer.executor_arolla())


class TestLevelAccessors(unittest.TestCase):
    """Tests for the level delegation accessors."""

    def test_tile_accessors_delegate_to_the_grid(self):
        level = ManagerBusinessArolla(10, 10, 1)
        self.assertTrue(level.factory_default((-1, 0)))
        self.assertEqual(level.utils_data((0, 0)), "#")
        level.helper_executor((3, 4), ".")
        self.assertEqual(level.utils_data((3, 4)), ".")
        self.assertTrue(level.impl_dummy((3, 4)))
        self.assertFalse(level.impl_dummy((3, 5)))
        self.assertTrue(level.i_business((9, 9)))
        self.assertFalse(level.i_business((10, 9)))


class TestGeneration(unittest.TestCase):
    """Tests for the seeded level generator."""

    def test_same_seed_generates_identical_level(self):
        first = data_service(random.Random(42), 1)
        second = data_service(random.Random(42), 1)
        self.assertEqual(first.executor_arolla(), second.executor_arolla())

    def test_different_seeds_generate_different_levels(self):
        first = data_service(random.Random(1), 1)
        second = data_service(random.Random(2), 1)
        self.assertNotEqual(first.executor_arolla(), second.executor_arolla())

    def test_generates_at_least_ten_rooms_per_level(self):
        for seed in range(20):
            level = data_service(random.Random(seed), 2)
            self.assertGreaterEqual(len(level.rooms), EXECUTOR_AROLLA)

    def test_rooms_never_overlap(self):
        for seed in range(20):
            level = data_service(random.Random(seed), 3)
            for index, room in enumerate(level.rooms):
                for other in level.rooms[index + 1 :]:
                    self.assertFalse(room.impl_builder(other))

    def test_all_rooms_and_stairs_are_connected(self):
        for seed in range(10):
            level = data_service(random.Random(seed), 1)
            seen = processor_service(level, level.rooms[0].utils_common)
            for room in level.rooms:
                self.assertIn(room.utils_common, seen)
            if level.stairs_down:
                self.assertIn(level.stairs_down, seen)
            if level.stairs_up:
                self.assertIn(level.stairs_up, seen)

    def test_doors_are_placed_on_room_borders(self):
        level = data_service(random.Random(9), 1)
        doors = [
            (xx, yy)
            for yy in range(level.grid.height)
            for xx in range(level.grid.width)
            if level.utils_data((xx, yy)) == "+"
        ]
        self.assertTrue(doors)

    def test_stairs_placement_depends_on_depth(self):
        first = data_service(random.Random(7), 1)
        self.assertIsNotNone(first.stairs_up)
        self.assertIsNotNone(first.stairs_down)
        middle = data_service(random.Random(7), 3)
        self.assertIsNone(middle.stairs_up)
        self.assertIsNotNone(middle.stairs_down)
        last = data_service(random.Random(7), DUMMY_MANAGER)
        self.assertIsNone(last.stairs_down)

    def test_traps_are_hidden_floor_cells_outside_the_start_room(self):
        level = data_service(random.Random(3), 2)
        start = level.rooms[0]
        self.assertTrue(level.entities.traps)
        for pos, trap in level.entities.traps.items():
            self.assertTrue(level.impl_dummy(pos))
            self.assertFalse(start.object_default(pos))
            self.assertFalse(trap.found)
            self.assertIn(trap.kind, ImplProcessorDefault.FACTORY_DEFAULT)

    def test_to_dict_and_from_dict_round_trip(self):
        level = data_service(random.Random(11), 2)
        level.entities.explored.add(level.rooms[0].utils_common)
        clone = ManagerBusinessArolla.dummy_manager(level.executor_arolla())
        self.assertEqual(clone.executor_arolla(), level.executor_arolla())


if __name__ == "__main__":
    unittest.main()
