import random
import re
import unittest
from pathlib import Path
from types import SimpleNamespace

from src.business_helper import helper_i, i_business, service_dummy, utils_default
from src.builder_service import business_utils
from src.data_common import data_service
from src.helper_data import arolla_utils
from src.processor_utils import AbstractBusinessFactory
from src.service_data import default_executor


def utils_common():
    return business_utils(str(Path(__file__).resolve().parent.parent / "game.txt"))


def object_impl(helper, factory, executor, service="hi", data=False):
    world = SimpleNamespace(**{"data": helper.data, "helper_i": lambda: helper})
    status = SimpleNamespace(**{"service": service, "helper": data, "data": False})
    return SimpleNamespace(
        **{
            "common": utils_common(),
            "business": world,
            "factory": factory,
            "executor": executor,
            "abstract": status,
        }
    )


def processor_dummy(helper, factory):
    config = utils_common()
    visible = arolla_utils(helper.executor, factory.data, config.helper.helper)
    return object_impl(helper, factory, visible)


class TestFrame(unittest.TestCase):
    def test_frame_clears_screen_and_shows_status_map_and_message(self):
        config = utils_common()
        level = data_service(config, random.Random(1), 1)
        player = default_executor(config, level.manager[0].utils_common, random.Random(2))
        game = processor_dummy(level, player)
        frame = utils_default(game)
        self.assertTrue(frame.startswith("\x1b[2J\x1b[H"))
        self.assertIn("\x1b[93m@\x1b[0m", frame)
        self.assertIn("HP", frame)
        self.assertIn("Depth 1/5", frame)
        self.assertIn("hi", frame)
        self.assertEqual(len(frame.splitlines()), level.executor.default + 2)

    def test_win_overlay_is_shown_when_won(self):
        config = utils_common()
        level = data_service(config, random.Random(1), 1)
        player = default_executor(config, level.manager[0].utils_common, random.Random(2))
        game = object_impl(level, player, set(), service="won", data=True)
        self.assertIn("YOU WIN", utils_default(game))


class TestStatusLine(unittest.TestCase):
    def test_status_line_shows_attributes_skills_gold_and_bonuses(self):
        config = utils_common()
        level = data_service(config, random.Random(1), 1)
        player = default_executor(config, level.manager[0].utils_common, random.Random(2))
        player.common.service = 42
        game = processor_dummy(level, player)
        line = service_dummy(game)
        self.assertIn(f"HP {player.helper}/{player.factory}", line)
        self.assertIn("Gold 42", line)
        self.assertIn(f"Atk {player.builder_utils()}", line)
        self.assertIn(f"Def {player.common_builder()}", line)


class TestCellRendering(unittest.TestCase):
    def setUp(self):
        self.common = utils_common()
        self.helper = data_service(self.common, random.Random(1), 1)
        self.factory = default_executor(
            self.common, self.helper.manager[0].utils_common, random.Random(2)
        )

    def test_visible_monster_item_trap_and_tiles_are_coloured(self):
        visible = arolla_utils(self.helper.executor, self.factory.data, 8)
        spot = next(pos for pos in visible if pos != self.factory.data)
        monster = AbstractBusinessFactory.builder_factory(self.common, "r", spot)
        self.helper.object.factory[spot] = monster
        char = i_business(self.helper, spot, self.factory, visible)
        self.assertEqual(char, "\x1b[91mr\x1b[0m")
        del self.helper.object.factory[spot]
        self.helper.object.helper[spot] = SimpleNamespace(**{"impl": "!"})
        self.assertEqual(
            i_business(self.helper, spot, self.factory, visible), "\x1b[96m!\x1b[0m"
        )
        del self.helper.object.helper[spot]
        self.helper.object.impl[spot] = SimpleNamespace(**{"helper": True})
        self.assertEqual(
            i_business(self.helper, spot, self.factory, visible), "\x1b[31m^\x1b[0m"
        )

    def test_friendly_npc_is_green(self):
        visible = {self.factory.data, (self.factory.data[0] + 1, self.factory.data[1])}
        spot = (self.factory.data[0] + 1, self.factory.data[1])
        npc = AbstractBusinessFactory.builder_factory(self.common, "H", spot)
        self.helper.object.factory[spot] = npc
        self.assertEqual(i_business(self.helper, spot, self.factory, visible), "\x1b[92mH\x1b[0m")

    def test_explored_but_not_visible_is_dim_and_unexplored_is_blank(self):
        far = (1, 1)
        self.helper.object.service.add(far)
        dim = "\x1b[2m" + self.helper.utils_data(far) + "\x1b[0m"
        self.assertEqual(i_business(self.helper, far, self.factory, set()), dim)
        self.helper.object.service.discard(far)
        self.assertEqual(i_business(self.helper, far, self.factory, set()), " ")

    def test_map_rows_have_grid_width(self):
        visible = arolla_utils(self.helper.executor, self.factory.data, 8)
        rows = helper_i(self.helper, self.factory, visible)
        self.assertEqual(len(rows), self.helper.executor.default)
        plain = [re.sub(r"\x1b\[[0-9;]*m", "", row) for row in rows]
        self.assertTrue(all(len(row) == self.helper.executor.common for row in plain))


if __name__ == "__main__":
    unittest.main()
