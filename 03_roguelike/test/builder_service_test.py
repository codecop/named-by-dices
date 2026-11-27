import tempfile
import unittest
from pathlib import Path

from src.builder_service import FactoryDataAbstract, abstract_business, business_utils

UTILS_BUILDER = Path(__file__).resolve().parent.parent / "game.txt"

SAMPLE = """
# a comment line

setting width 40
setting max_depth 3
monster r rat 3 2 0 2 1
monster D big dragon 30 10 3 100 3
npc H old hermit 12
item weapon ) short sword 2
item potion ! healing potion 6
trap dart
"""


def utils_common():
    return business_utils(str(UTILS_BUILDER))


class TestParseConfig(unittest.TestCase):
    def test_settings_are_parsed(self):
        game = abstract_business(SAMPLE)
        self.assertEqual(game.helper.common, 40)
        self.assertEqual(game.helper.data, 3)
        self.assertEqual(game.helper.default, 22)

    def test_monsters_keep_letter_name_and_numbers(self):
        game = abstract_business(SAMPLE)
        self.assertEqual(game.manager["r"], ("rat", 3, 2, 0, 2, 1))
        self.assertEqual(game.manager["D"], ("big dragon", 30, 10, 3, 100, 3))

    def test_npc_is_registered_as_monster_and_friendly(self):
        game = abstract_business(SAMPLE)
        self.assertEqual(game.service["H"], ("old hermit", 12))
        self.assertIn("H", game.manager)

    def test_items_keep_kind_letter_name_and_power(self):
        game = abstract_business(SAMPLE)
        self.assertEqual(game.object["weapon"], [(")", "short sword", 2)])
        self.assertEqual(game.object["potion"], [("!", "healing potion", 6)])

    def test_traps_are_collected(self):
        game = abstract_business(SAMPLE)
        self.assertEqual(game.processor, ["dart"])

    def test_unknown_directive_raises_with_line_number(self):
        with self.assertRaises(ValueError) as ctx:
            abstract_business("monster r rat 3 2 0 2 1\nbogus x\n")
        self.assertIn("line 2", str(ctx.exception))

    def test_non_numeric_value_raises_with_line_number(self):
        with self.assertRaises(ValueError) as ctx:
            abstract_business("setting width lots\n")
        self.assertIn("line 1", str(ctx.exception))

    def test_short_monster_line_raises(self):
        with self.assertRaises(ValueError):
            abstract_business("monster r rat 3\n")

    def test_unknown_setting_raises(self):
        with self.assertRaises(ValueError) as ctx:
            abstract_business("setting colour 5\n")
        self.assertIn("unknown setting", str(ctx.exception))

    def test_setting_with_wrong_arg_count_raises(self):
        with self.assertRaises(ValueError):
            abstract_business("setting width\n")

    def test_short_npc_line_raises(self):
        with self.assertRaises(ValueError):
            abstract_business("npc H\n")

    def test_short_item_line_raises(self):
        with self.assertRaises(ValueError):
            abstract_business("item weapon )\n")

    def test_trap_with_extra_word_raises(self):
        with self.assertRaises(ValueError):
            abstract_business("trap dart now\n")


class TestLoadConfig(unittest.TestCase):
    def test_shipped_game_txt_loads_with_all_sections(self):
        game = utils_common()
        self.assertEqual(game.helper.common, 78)
        self.assertEqual(game.helper.data, 5)
        self.assertEqual(game.manager["D"], ("dragon", 30, 10, 3, 100, 5))
        self.assertIn("H", game.service)
        self.assertIn("weapon", game.object)
        self.assertIn("artefact", game.object)
        self.assertIn("dart", game.processor)

    def test_load_from_a_real_file(self):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", delete=False, encoding="utf-8"
        ) as handle:
            handle.write(SAMPLE)
            path = handle.name
        game = business_utils(path)
        self.assertEqual(game.helper.common, 40)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            business_utils("no-such-file.txt")

    def test_to_dict_and_from_dict_round_trip(self):
        game = utils_common()
        clone = FactoryDataAbstract.dummy_manager(game.executor_arolla())
        self.assertEqual(clone.executor_arolla(), game.executor_arolla())


if __name__ == "__main__":
    unittest.main()
