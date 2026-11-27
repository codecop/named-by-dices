"""Unit tests for src/manager_common.py."""

import random
import unittest

from src.manager_common import FACTORY_DUMMY, ObjectDummyService, executor_factory, factory_arolla, object_arolla


class TestItem(unittest.TestCase):
    """Tests for the item value object."""

    def test_describe_returns_the_display_name(self):
        item = ObjectDummyService("!", "healing potion", "potion", 6)
        self.assertEqual(item.manager_abstract(), "healing potion")

    def test_to_dict_and_from_dict_round_trip(self):
        item = ObjectDummyService("/", "wand of magic missile", "wand", 5, 5)
        clone = factory_arolla(item.data_manager())
        self.assertEqual(clone.data_manager(), item.data_manager())

    def test_artefact_is_the_unique_golden_die(self):
        artefact = object_arolla()
        self.assertEqual(artefact.impl, "&")
        self.assertEqual(artefact.data, "artefact")
        clone = factory_arolla(artefact.data_manager())
        self.assertEqual(clone.manager_abstract(), "the Golden Die")


class TestRandomItem(unittest.TestCase):
    """Tests for the random item factory."""

    def test_generated_items_have_a_known_kind_and_matching_letter(self):
        rng = random.Random(7)
        letters = {kind: {entry[0] for entry in entries} for kind, entries in FACTORY_DUMMY.items()}
        for _ in range(200):
            item = executor_factory(rng, 1)
            self.assertIn(item.data, FACTORY_DUMMY)
            self.assertIn(item.impl, letters[item.data])

    def test_weapons_and_armour_get_better_with_depth(self):
        rng = random.Random(11)
        shallow = [executor_factory(rng, 1) for _ in range(200)]
        rng = random.Random(11)
        deep = [executor_factory(rng, 5) for _ in range(200)]
        shallow_power = [item.helper for item in shallow if item.data in ("weapon", "armour")]
        deep_power = [item.helper for item in deep if item.data in ("weapon", "armour")]
        self.assertGreater(min(deep_power), min(shallow_power))

    def test_gold_amount_scales_with_depth_and_wands_have_charges(self):
        rng = random.Random(3)
        for _ in range(100):
            item = executor_factory(rng, 4)
            if item.data == "gold":
                self.assertGreaterEqual(item.helper, 40)
            if item.data == "wand":
                self.assertEqual(item.factory, item.helper)
                self.assertGreater(item.factory, 0)

    def test_same_seed_generates_the_same_item(self):
        first = executor_factory(random.Random(9), 2)
        second = executor_factory(random.Random(9), 2)
        self.assertEqual(first.data_manager(), second.data_manager())


if __name__ == "__main__":
    unittest.main()
