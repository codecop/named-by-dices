import random
import unittest
from pathlib import Path

from src.builder_service import business_utils
from src.manager_common import ObjectDummyService, executor_factory, factory_arolla, object_arolla


def utils_common():
    return business_utils(str(Path(__file__).resolve().parent.parent / "game.txt"))


class TestItem(unittest.TestCase):
    def test_describe_returns_the_display_name(self):
        item = ObjectDummyService("!", "healing potion", "potion", 6)
        self.assertEqual(item.manager_abstract(), "healing potion")

    def test_to_dict_and_from_dict_round_trip(self):
        item = ObjectDummyService("/", "wand of magic missile", "wand", 5, 5)
        clone = factory_arolla(item.data_manager())
        self.assertEqual(clone.data_manager(), item.data_manager())

    def test_artefact_comes_from_the_config(self):
        artefact = object_arolla(utils_common())
        self.assertEqual(artefact.impl, "&")
        self.assertEqual(artefact.data, "artefact")
        self.assertEqual(artefact.manager_abstract(), "the Golden Die")


class TestRandomItem(unittest.TestCase):
    def test_generated_items_have_a_known_kind_and_matching_letter(self):
        config = utils_common()
        letters = {
            kind: {entry[0] for entry in entries} for kind, entries in config.object.items()
        }
        rng = random.Random(7)
        for _ in range(200):
            item = executor_factory(config, rng, 1)
            self.assertIn(item.data, config.object)
            self.assertIn(item.impl, letters[item.data])

    def test_weapons_and_armour_get_better_with_depth(self):
        config = utils_common()
        rng = random.Random(11)
        shallow = [executor_factory(config, rng, 1) for _ in range(200)]
        rng = random.Random(11)
        deep = [executor_factory(config, rng, 5) for _ in range(200)]
        shallow_power = [i.helper for i in shallow if i.data in ("weapon", "armour")]
        deep_power = [i.helper for i in deep if i.data in ("weapon", "armour")]
        self.assertGreater(min(deep_power), min(shallow_power))

    def test_gold_amount_scales_with_depth_and_wands_have_charges(self):
        config = utils_common()
        rng = random.Random(3)
        for _ in range(100):
            item = executor_factory(config, rng, 4)
            if item.data == "gold":
                self.assertGreaterEqual(item.helper, 40)
            if item.data == "wand":
                self.assertEqual(item.factory, item.helper)
                self.assertGreater(item.factory, 0)

    def test_same_seed_generates_the_same_item(self):
        config = utils_common()
        first = executor_factory(config, random.Random(9), 2)
        second = executor_factory(config, random.Random(9), 2)
        self.assertEqual(first.data_manager(), second.data_manager())


if __name__ == "__main__":
    unittest.main()
