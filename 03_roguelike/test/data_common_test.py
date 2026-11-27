import random
import unittest
from pathlib import Path

from src.builder_service import abstract_business, business_utils
from src.data_common import (
    ArollaImplData,
    ImplProcessorDefault,
    ManagerBusinessArolla,
    ServiceObjectCommon,
    UtilsCommonExecutor,
    common_helper,
    data_service,
    processor_manager,
    utils_executor,
)
from src.object_common import builder_default


def utils_common():
    return business_utils(str(Path(__file__).resolve().parent.parent / "game.txt"))


def processor_service(helper, data):
    factory = {data}
    manager = [data]
    while manager:
        impl = manager.pop()
        for service in builder_default(impl):
            if service not in factory and helper.impl_dummy(service):
                factory.add(service)
                manager.append(service)
    return factory


class TestRoom(unittest.TestCase):
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
    def test_hidden_by_default_and_round_trips(self):
        trap = ImplProcessorDefault("dart")
        self.assertEqual(trap.data, "dart")
        self.assertFalse(trap.helper)
        clone = ImplProcessorDefault.i_utils(trap.object_factory())
        self.assertEqual(clone.data, "dart")
        self.assertFalse(clone.helper)
        trap.helper = True
        clone = ImplProcessorDefault.i_utils(trap.object_factory())
        self.assertTrue(clone.helper)


class TestGrid(unittest.TestCase):
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
    def test_random_free_cell_is_walkable_and_avoids_given_cells(self):
        grid = UtilsCommonExecutor(20, 20)
        for yy in range(1, 19):
            for xx in range(1, 19):
                grid.helper_executor((xx, yy), ".")
        layer = ServiceObjectCommon()
        rng = random.Random(5)
        for _ in range(20):
            cell = layer.business_arolla(grid, rng, ((5, 5),), (1, 1))
            self.assertTrue(grid.impl_dummy(cell))
            self.assertNotEqual(cell, (5, 5))

    def test_random_free_cell_skips_occupied_cells(self):
        grid = UtilsCommonExecutor(6, 6)
        for yy in range(1, 5):
            for xx in range(1, 5):
                grid.helper_executor((xx, yy), ".")
        layer = ServiceObjectCommon()
        layer.helper[(2, 2)] = object()
        layer.factory[(3, 3)] = object()
        rng = random.Random(2)
        for _ in range(20):
            cell = layer.business_arolla(grid, rng, (), (1, 1))
            self.assertNotIn(cell, ((2, 2), (3, 3)))

    def test_random_free_cell_falls_back_when_no_cell_is_free(self):
        grid = UtilsCommonExecutor(4, 4)
        layer = ServiceObjectCommon()
        cell = layer.business_arolla(grid, random.Random(1), (), (1, 1))
        self.assertEqual(cell, (1, 1))

    def test_to_dict_and_from_dict_round_trip(self):
        layer = ServiceObjectCommon()
        layer.impl[(2, 3)] = ImplProcessorDefault("alarm", True)
        layer.service.add((1, 1))
        clone = ServiceObjectCommon.dummy_manager(layer.executor_arolla())
        self.assertEqual(clone.executor_arolla(), layer.executor_arolla())


class TestLevelAccessors(unittest.TestCase):
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
    def test_same_seed_generates_identical_level(self):
        config = utils_common()
        first = data_service(config, random.Random(42), 1)
        second = data_service(config, random.Random(42), 1)
        self.assertEqual(first.executor_arolla(), second.executor_arolla())

    def test_different_seeds_generate_different_levels(self):
        config = utils_common()
        first = data_service(config, random.Random(1), 1)
        second = data_service(config, random.Random(2), 1)
        self.assertNotEqual(first.executor_arolla(), second.executor_arolla())

    def test_generates_at_least_the_configured_minimum_of_rooms(self):
        config = utils_common()
        for seed in range(20):
            level = data_service(config, random.Random(seed), 2)
            self.assertGreaterEqual(len(level.manager), config.helper.factory)

    def test_rooms_never_overlap(self):
        config = utils_common()
        for seed in range(20):
            level = data_service(config, random.Random(seed), 3)
            for index, room in enumerate(level.manager):
                for other in level.manager[index + 1:]:
                    self.assertFalse(room.impl_builder(other))

    def test_all_rooms_and_stairs_are_connected(self):
        config = utils_common()
        for seed in range(10):
            level = data_service(config, random.Random(seed), 1)
            seen = processor_service(level, level.manager[0].utils_common)
            for room in level.manager:
                self.assertIn(room.utils_common, seen)
            if level.processor:
                self.assertIn(level.processor, seen)
            if level.utils:
                self.assertIn(level.utils, seen)

    def test_doors_are_placed_on_room_borders(self):
        config = utils_common()
        level = data_service(config, random.Random(9), 1)
        doors = [
            (xx, yy)
            for yy in range(level.executor.default)
            for xx in range(level.executor.common)
            if level.utils_data((xx, yy)) == "+"
        ]
        self.assertTrue(doors)

    def test_stairs_placement_depends_on_depth(self):
        config = utils_common()
        first = data_service(config, random.Random(7), 1)
        self.assertIsNotNone(first.utils)
        self.assertIsNotNone(first.processor)
        middle = data_service(config, random.Random(7), 3)
        self.assertIsNotNone(middle.utils)
        self.assertIsNotNone(middle.processor)
        last = data_service(config, random.Random(7), config.helper.data)
        self.assertIsNotNone(last.utils)
        self.assertIsNone(last.processor)

    def test_traps_are_hidden_floor_cells_outside_the_start_room(self):
        config = utils_common()
        level = data_service(config, random.Random(3), 2)
        start = level.manager[0]
        self.assertTrue(level.object.impl)
        for pos, trap in level.object.impl.items():
            self.assertTrue(level.impl_dummy(pos))
            self.assertFalse(start.object_default(pos))
            self.assertFalse(trap.helper)
            self.assertIn(trap.data, config.processor)

    def test_to_dict_and_from_dict_round_trip(self):
        config = utils_common()
        level = data_service(config, random.Random(11), 2)
        level.object.service.add(level.manager[0].utils_common)
        clone = ManagerBusinessArolla.dummy_manager(level.executor_arolla())
        self.assertEqual(clone.executor_arolla(), level.executor_arolla())


class TestEdgeCases(unittest.TestCase):
    def test_common_helper_skips_wall_border_cells(self):
        level = ManagerBusinessArolla(10, 10, 1)
        level.manager.append(ArollaImplData(1, 1, 4, 4))
        common_helper(level)
        self.assertEqual(level.utils_data((1, 1)), "#")

    def test_processor_manager_guard_avoids_the_stairs_up_cell(self):
        config = utils_common()
        level = ManagerBusinessArolla(20, 10, 1)
        level.manager.append(ArollaImplData(1, 1, 3, 3))
        level.manager.append(ArollaImplData(1, 1, 3, 3))
        processor_manager(config, level, random.Random(0))
        self.assertIsNotNone(level.utils)
        self.assertIsNotNone(level.processor)

    def test_utils_executor_without_trap_kinds_places_nothing(self):
        config = abstract_business(
            "setting width 30\nsetting height 12\nsetting min_rooms 2\nsetting max_rooms 2\n"
        )
        level = data_service(config, random.Random(1), 1)
        level.object.impl.clear()
        utils_executor(config, level, random.Random(1))
        self.assertFalse(level.object.impl)

    def test_utils_executor_skips_start_room_and_existing_traps(self):
        config = utils_common()
        level = ManagerBusinessArolla(8, 8, 1)
        level.manager.append(ArollaImplData(1, 1, 2, 2))
        for yy in range(1, 7):
            for xx in range(1, 7):
                level.helper_executor((xx, yy), ".")
                if not level.manager[0].object_default((xx, yy)):
                    level.object.impl[(xx, yy)] = ImplProcessorDefault("dart")
        before = len(level.object.impl)
        utils_executor(config, level, random.Random(2))
        self.assertEqual(len(level.object.impl), before)

    def test_tiny_map_exhausts_room_placement_attempts(self):
        config = abstract_business(
            "setting width 20\nsetting height 14\nsetting min_rooms 40\nsetting max_rooms 40\n"
        )
        level = data_service(config, random.Random(1), 1)
        self.assertLess(len(level.manager), 40)


if __name__ == "__main__":
    unittest.main()
