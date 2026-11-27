"""Unit tests for src/service_data.py."""

import random
import unittest

from src.manager_common import ObjectDummyService
from src.service_data import (
    AbstractUtilsData,
    BusinessHelperCommon,
    BusinessServiceArolla,
    DefaultObjectManager,
    default_executor,
)


def utils_common(letter="!", name="healing potion", kind="potion", power=6, charges=0):
    """Build a test item (test helper)."""
    return ObjectDummyService(letter, name, kind, power, charges)


class TestAttributesAndSkills(unittest.TestCase):
    """Tests for the attribute and skill containers."""

    def test_attributes_round_trip(self):
        attributes = AbstractUtilsData(10, 11, 12)
        clone = AbstractUtilsData.business_i(attributes.data_default())
        self.assertEqual(clone.data_default(), attributes.data_default())

    def test_skills_round_trip(self):
        skills = BusinessHelperCommon(1, 2, 3)
        clone = BusinessHelperCommon.service_abstract(skills.manager_data())
        self.assertEqual(clone.manager_data(), skills.manager_data())


class TestInventory(unittest.TestCase):
    """Tests for the inventory container."""

    def test_add_appends_items(self):
        inventory = DefaultObjectManager()
        item = utils_common()
        inventory.impl_common(item)
        self.assertEqual(inventory.items, [item])

    def test_wield_moves_item_from_inventory_and_swaps_old_weapon_back(self):
        inventory = DefaultObjectManager()
        first = utils_common(")", "dagger", "weapon", 1)
        second = utils_common(")", "battle axe", "weapon", 3)
        inventory.impl_common(first)
        inventory.impl_common(second)
        inventory.utils_i(first)
        self.assertIs(inventory.weapon, first)
        self.assertEqual(inventory.items, [second])
        inventory.utils_i(second)
        self.assertIs(inventory.weapon, second)
        self.assertEqual(inventory.items, [first])

    def test_wear_moves_item_from_inventory_and_swaps_old_armour_back(self):
        inventory = DefaultObjectManager()
        first = utils_common("[", "leather armour", "armour", 1)
        second = utils_common("[", "chain mail", "armour", 2)
        inventory.impl_common(first)
        inventory.impl_common(second)
        inventory.executor_i(first)
        self.assertIs(inventory.armour, first)
        inventory.executor_i(second)
        self.assertIs(inventory.armour, second)
        self.assertEqual(inventory.items, [first])

    def test_to_dict_and_from_dict_round_trip(self):
        inventory = DefaultObjectManager()
        inventory.impl_common(utils_common())
        inventory.utils_i(utils_common(")", "sword", "weapon", 2))
        inventory.gold = 50
        clone = DefaultObjectManager.dummy_manager(inventory.executor_arolla())
        self.assertEqual(clone.executor_arolla(), inventory.executor_arolla())


class TestPlayer(unittest.TestCase):
    """Tests for the player character."""

    def test_new_player_starts_at_full_hp_with_constitution_based_max_hp(self):
        player = default_executor((2, 3), random.Random(3))
        self.assertEqual(player.letter, "@")
        self.assertEqual(player.pos, (2, 3))
        self.assertEqual(player.hp, player.max_hp)
        self.assertEqual(player.max_hp, 8 + player.attributes.constitution)
        self.assertEqual(player.xp, 0)
        self.assertEqual(player.level, 1)

    def test_attack_bonus_combines_strength_skill_and_weapon(self):
        player = default_executor((0, 0), random.Random(1))
        player.attributes.strength = 12
        player.skills.fighting = 2
        expected = 12 // 3 + 2
        self.assertEqual(player.builder_utils(), expected)
        player.inventory.utils_i(utils_common(")", "sword", "weapon", 4))
        self.assertEqual(player.builder_utils(), expected + 4)

    def test_defence_bonus_combines_dexterity_skill_and_armour(self):
        player = default_executor((0, 0), random.Random(1))
        player.attributes.dexterity = 9
        player.skills.dodging = 1
        expected = 9 // 3 + 1
        self.assertEqual(player.common_builder(), expected)
        player.inventory.executor_i(utils_common("[", "chain mail", "armour", 2))
        self.assertEqual(player.common_builder(), expected + 2)

    def test_gain_xp_levels_up_and_improves_the_character(self):
        player = default_executor((0, 0), random.Random(1))
        old_max_hp = player.max_hp
        gained = player.arolla_utils(20)
        self.assertEqual(gained, 1)
        self.assertEqual(player.level, 2)
        self.assertEqual(player.max_hp, old_max_hp + 3)
        self.assertGreater(player.attributes.strength, 8)
        gained = player.arolla_utils(100)
        self.assertGreaterEqual(gained, 2)
        self.assertGreaterEqual(player.level, 4)

    def test_to_dict_and_from_dict_round_trip(self):
        player = default_executor((4, 5), random.Random(8))
        player.inventory.impl_common(utils_common())
        player.inventory.utils_i(utils_common(")", "axe", "weapon", 3))
        player.inventory.gold = 25
        player.arolla_utils(25)
        player.utils_data(4)
        clone = BusinessServiceArolla.service_abstract(player.data_manager())
        self.assertEqual(clone.data_manager(), player.data_manager())


if __name__ == "__main__":
    unittest.main()
