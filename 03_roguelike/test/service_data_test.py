import random
import unittest
from pathlib import Path

from src.builder_service import business_utils
from src.manager_common import ObjectDummyService
from src.service_data import (
    AbstractUtilsData,
    BusinessHelperCommon,
    BusinessServiceArolla,
    DefaultObjectManager,
    default_executor,
)


def utils_common():
    return business_utils(str(Path(__file__).resolve().parent.parent / "game.txt"))


def service_builder(impl="!", service="healing potion", data="potion", helper=6, factory=0):
    return ObjectDummyService(impl, service, data, helper, factory)


class TestAttributesAndSkills(unittest.TestCase):
    def test_attributes_round_trip(self):
        attributes = AbstractUtilsData(10, 11, 12)
        clone = AbstractUtilsData.business_i(attributes.data_default())
        self.assertEqual(clone.data_default(), attributes.data_default())

    def test_skills_round_trip(self):
        skills = BusinessHelperCommon(1, 2, 3)
        clone = BusinessHelperCommon.service_abstract(skills.manager_data())
        self.assertEqual(clone.manager_data(), skills.manager_data())


class TestInventory(unittest.TestCase):
    def test_add_appends_items(self):
        inventory = DefaultObjectManager()
        item = service_builder()
        inventory.impl_common(item)
        self.assertEqual(inventory.factory, [item])

    def test_wield_moves_item_from_inventory_and_swaps_old_weapon_back(self):
        inventory = DefaultObjectManager()
        first = service_builder(")", "dagger", "weapon", 1)
        second = service_builder(")", "battle axe", "weapon", 3)
        inventory.impl_common(first)
        inventory.impl_common(second)
        inventory.utils_i(first)
        self.assertIs(inventory.helper, first)
        self.assertEqual(inventory.factory, [second])
        inventory.utils_i(second)
        self.assertIs(inventory.helper, second)
        self.assertEqual(inventory.factory, [first])

    def test_wear_moves_item_from_inventory_and_swaps_old_armour_back(self):
        inventory = DefaultObjectManager()
        first = service_builder("[", "leather armour", "armour", 1)
        second = service_builder("[", "chain mail", "armour", 2)
        inventory.impl_common(first)
        inventory.impl_common(second)
        inventory.executor_i(first)
        self.assertIs(inventory.impl, first)
        inventory.executor_i(second)
        self.assertIs(inventory.impl, second)
        self.assertEqual(inventory.factory, [first])

    def test_to_dict_and_from_dict_round_trip(self):
        inventory = DefaultObjectManager()
        inventory.impl_common(service_builder())
        inventory.utils_i(service_builder(")", "sword", "weapon", 2))
        inventory.service = 50
        clone = DefaultObjectManager.dummy_manager(inventory.executor_arolla())
        self.assertEqual(clone.executor_arolla(), inventory.executor_arolla())


class TestPlayer(unittest.TestCase):
    def test_new_player_starts_at_full_hp_with_constitution_based_max_hp(self):
        config = utils_common()
        player = default_executor(config, (2, 3), random.Random(3))
        self.assertEqual(player.impl, "@")
        self.assertEqual(player.data, (2, 3))
        self.assertEqual(player.helper, player.factory)
        self.assertEqual(player.factory, config.helper.service + player.builder.common)
        self.assertEqual(player.abstract, 0)
        self.assertEqual(player.arolla, 1)

    def test_attack_bonus_combines_strength_skill_and_weapon(self):
        config = utils_common()
        player = default_executor(config, (0, 0), random.Random(1))
        player.builder.builder = 12
        player.business.data = 2
        expected = 12 // 3 + 2
        self.assertEqual(player.builder_utils(), expected)
        player.common.utils_i(service_builder(")", "sword", "weapon", 4))
        self.assertEqual(player.builder_utils(), expected + 4)

    def test_defence_bonus_combines_dexterity_skill_and_armour(self):
        config = utils_common()
        player = default_executor(config, (0, 0), random.Random(1))
        player.builder.business = 9
        player.business.helper = 1
        expected = 9 // 3 + 1
        self.assertEqual(player.common_builder(), expected)
        player.common.executor_i(service_builder("[", "chain mail", "armour", 2))
        self.assertEqual(player.common_builder(), expected + 2)

    def test_gain_xp_levels_up_and_improves_the_character(self):
        config = utils_common()
        player = default_executor(config, (0, 0), random.Random(1))
        old_max = player.factory
        old_strength = player.builder.builder
        gained = player.arolla_utils(20)
        self.assertEqual(gained, 1)
        self.assertEqual(player.arolla, 2)
        self.assertEqual(player.factory, old_max + 3)
        self.assertGreater(player.builder.builder, old_strength)
        gained = player.arolla_utils(100)
        self.assertGreaterEqual(gained, 2)
        self.assertGreaterEqual(player.arolla, 4)

    def test_to_dict_and_from_dict_round_trip(self):
        config = utils_common()
        player = default_executor(config, (4, 5), random.Random(8))
        player.common.impl_common(service_builder())
        player.common.utils_i(service_builder(")", "axe", "weapon", 3))
        player.common.service = 25
        player.arolla_utils(25)
        player.utils_data(4)
        clone = BusinessServiceArolla.service_abstract(config, player.data_manager())
        self.assertEqual(clone.data_manager(), player.data_manager())


if __name__ == "__main__":
    unittest.main()
