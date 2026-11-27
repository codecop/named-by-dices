import random
import unittest
from pathlib import Path

from src.builder_service import business_utils
from src.data_common import ArollaImplData, ManagerBusinessArolla, data_service
from src.processor_utils import (
    AbstractBusinessFactory,
    arolla_executor,
    dummy_processor,
    helper_builder,
    processor_service,
)


def utils_common():
    return business_utils(str(Path(__file__).resolve().parent.parent / "game.txt"))


def object_factory(level, letter, pos):
    monster = AbstractBusinessFactory.builder_factory(utils_common(), letter, pos)
    level.object.factory[pos] = monster
    return monster


class TestMonster(unittest.TestCase):
    def test_factory_builds_stats_from_the_config(self):
        monster = AbstractBusinessFactory.builder_factory(utils_common(), "r", (1, 1))
        self.assertEqual(monster.impl, "r")
        self.assertEqual(monster.service, "rat")
        self.assertEqual(monster.helper, 3)
        self.assertEqual(monster.manager, 2)
        self.assertEqual(monster.executor, 0)
        self.assertEqual(monster.object, 2)
        self.assertFalse(monster.processor)

    def test_npc_letter_is_friendly(self):
        monster = AbstractBusinessFactory.builder_factory(utils_common(), "H", (1, 1))
        self.assertTrue(monster.processor)
        self.assertEqual(monster.manager, 0)

    def test_to_dict_and_from_dict_round_trip(self):
        monster = AbstractBusinessFactory.builder_factory(utils_common(), "T", (2, 2))
        monster.utils_data(4)
        clone = dummy_processor(monster.executor_common())
        self.assertEqual(clone.executor_common(), monster.executor_common())


class TestSpawning(unittest.TestCase):
    def test_monsters_spawn_outside_the_start_room_on_floor(self):
        config = utils_common()
        level = data_service(config, random.Random(5), 2)
        processor_service(config, level, random.Random(6), 2)
        start = level.manager[0]
        self.assertGreaterEqual(len(level.object.factory), 6)
        for pos, monster in level.object.factory.items():
            self.assertTrue(level.impl_dummy(pos))
            self.assertFalse(start.object_default(pos))
            self.assertNotIn(monster.impl, config.service)

    def test_deeper_levels_spawn_more_monsters(self):
        config = utils_common()
        shallow = data_service(config, random.Random(5), 1)
        processor_service(config, shallow, random.Random(6), 1)
        deep = data_service(config, random.Random(5), 5)
        processor_service(config, deep, random.Random(6), 5)
        self.assertGreater(len(deep.object.factory), len(shallow.object.factory))

    def test_helper_npc_is_placed_outside_the_start_room(self):
        config = utils_common()
        level = data_service(config, random.Random(5), 2)
        helper_builder(config, level, random.Random(6))
        npcs = [m for m in level.object.factory.values() if m.processor]
        self.assertEqual(len(npcs), 1)
        self.assertFalse(level.manager[0].object_default(npcs[0].data))


class TestChooseMove(unittest.TestCase):
    def open_level(self):
        level = ManagerBusinessArolla(10, 10, 1)
        level.manager.append(ArollaImplData(1, 1, 8, 8))
        for yy in range(1, 9):
            for xx in range(1, 9):
                level.helper_executor((xx, yy), ".")
        return level

    def test_seen_target_is_chased(self):
        level = self.open_level()
        monster = object_factory(level, "r", (5, 5))
        step = arolla_executor(random.Random(1), level, monster, (5, 1), True)
        self.assertEqual(step, (5, 4))

    def test_adjacent_seen_target_is_attacked(self):
        level = self.open_level()
        monster = object_factory(level, "r", (5, 5))
        step = arolla_executor(random.Random(1), level, monster, (5, 4), True)
        self.assertEqual(step, (5, 4))

    def test_wall_blocks_the_chase(self):
        level = self.open_level()
        level.helper_executor((5, 4), "#")
        monster = object_factory(level, "r", (5, 5))
        step = arolla_executor(random.Random(1), level, monster, (5, 1), True)
        self.assertNotEqual(step, (5, 4))

    def test_unseen_target_means_wander_or_stay(self):
        level = self.open_level()
        monster = object_factory(level, "r", (5, 5))
        step = arolla_executor(random.Random(1), level, monster, (1, 1), False)
        self.assertTrue(step == (5, 5) or level.impl_dummy(step))
        self.assertNotEqual(step, (1, 1))


if __name__ == "__main__":
    unittest.main()
