import random
import unittest
from pathlib import Path

from src.builder_dummy import helper_arolla, impl_common
from src.builder_service import abstract_business, business_utils
from src.data_common import ImplProcessorDefault, data_service
from src.impl_object import (
    UTILS_DEFAULT,
    ArollaBusinessFactory,
    ManagerIExecutor,
    default_service,
)
from src.manager_common import ObjectDummyService, object_arolla
from src.processor_utils import AbstractBusinessFactory


def utils_common():
    return business_utils(str(Path(__file__).resolve().parent.parent / "game.txt"))


def object_impl(common, data, utils):
    factory = iter(list(utils) + [""] * 50)
    manager = []
    processor = []
    executor = ArollaBusinessFactory(factory.__next__, manager.append, processor.append)
    service = ManagerIExecutor(common, data, executor)
    return service, manager, processor


def dummy_helper(service):
    helper = service.business.helper_i()
    data = service.factory.data
    for impl, builder in UTILS_DEFAULT.items():
        factory = (data[0] + builder[0], data[1] + builder[1])
        if helper.impl_dummy(factory) and factory not in helper.object.factory:
            return impl, factory
    raise AssertionError("no free neighbour")


class TestNewGame(unittest.TestCase):
    def test_new_game_has_level_player_monsters_npc_and_items(self):
        config = utils_common()
        game, _, _ = object_impl(config, 7, [])
        level = game.business.helper_i()
        self.assertEqual(game.business.data, 1)
        self.assertGreaterEqual(len(level.manager), config.helper.factory)
        self.assertEqual(game.factory.data, level.manager[0].utils_common)
        self.assertTrue(level.object.factory)
        self.assertTrue(any(m.processor for m in level.object.factory.values()))
        self.assertTrue(level.object.helper)
        game.impl_business()
        self.assertTrue(game.executor)

    def test_deepest_level_gets_artefact_and_boss(self):
        config = utils_common()
        level = data_service(config, random.Random(3), config.helper.data)
        default_service(config, level, random.Random(4), config.helper.data)
        kinds = [item.data for item in level.object.helper.values()]
        self.assertIn("artefact", kinds)
        self.assertTrue(any(m.impl == "D" for m in level.object.factory.values()))


class TestMovement(unittest.TestCase):
    def setUp(self):
        self.common = utils_common()
        self.service, self.factory, self.manager = object_impl(self.common, 7, [])

    def test_move_into_wall_keeps_position(self):
        self.service.factory.data = (0, 0)
        self.service.helper_executor("l")
        self.assertEqual(self.service.factory.data, (0, 0))
        self.assertEqual(self.service.abstract.service, "A wall.")

    def test_move_onto_floor_moves_player(self):
        key, target = dummy_helper(self.service)
        self.service.helper_executor(key)
        self.assertEqual(self.service.factory.data, target)

    def test_attack_kills_monster_and_grants_xp(self):
        key, target = dummy_helper(self.service)
        level = self.service.business.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.common, "r", target)
        level.object.factory[target] = monster
        for _ in range(10):
            self.service.helper_executor(key)
            if target not in level.object.factory:
                break
        self.assertNotIn(target, level.object.factory)
        self.assertGreater(self.service.factory.abstract, 0)

    def test_friendly_npc_heals_once_then_gives_advice(self):
        key, target = dummy_helper(self.service)
        level = self.service.business.helper_i()
        npc = AbstractBusinessFactory.builder_factory(self.common, "H", target)
        level.object.factory[target] = npc
        self.service.factory.helper = 1
        self.service.helper_executor(key)
        self.assertEqual(self.service.factory.helper, self.service.factory.factory)
        self.assertTrue(npc.utils)
        self.service.helper_executor(key)
        self.assertIn("Golden Die", self.service.abstract.service)

    def test_pickup_item_gold_and_artefact(self):
        level = self.service.business.helper_i()
        pos = self.service.factory.data
        level.object.helper[pos] = ObjectDummyService("!", "healing potion", "potion", 6)
        self.service.helper_executor(",")
        self.assertEqual(len(self.service.factory.common.factory), 1)
        self.assertNotIn(pos, level.object.helper)
        level.object.helper[pos] = ObjectDummyService("$", "pile of gold", "gold", 30)
        self.service.helper_executor(",")
        self.assertEqual(self.service.factory.common.service, 30)
        level.object.helper[pos] = object_arolla(self.common)
        self.service.helper_executor(",")
        self.assertEqual(self.service.abstract.service, impl_common("amulet"))
        self.service.helper_executor(",")
        self.assertEqual(self.service.abstract.service, "Nothing here.")

    def test_teleport_trap_moves_player_and_is_found(self):
        key, target = dummy_helper(self.service)
        level = self.service.business.helper_i()
        old = self.service.factory.data
        level.object.impl[target] = ImplProcessorDefault("teleport")
        self.service.helper_executor(key)
        self.assertTrue(level.object.impl[target].helper)
        self.assertNotEqual(self.service.factory.data, old)
        self.assertIn("teleport", self.service.abstract.service)

    def test_dart_trap_damages_player(self):
        target = dummy_helper(self.service)[1]
        key = dummy_helper(self.service)[0]
        level = self.service.business.helper_i()
        level.object.impl[target] = ImplProcessorDefault("dart")
        before = self.service.factory.helper
        self.service.helper_executor(key)
        self.assertTrue(level.object.impl[target].helper)
        self.assertLessEqual(self.service.factory.helper, before)

    def test_alarm_trap_spawns_monsters(self):
        key, target = dummy_helper(self.service)
        level = self.service.business.helper_i()
        before = len(level.object.factory)
        level.object.impl[target] = ImplProcessorDefault("alarm")
        self.service.helper_executor(key)
        self.assertEqual(len(level.object.factory), before + 2)


class TestItems(unittest.TestCase):
    def setUp(self):
        self.common = utils_common()
        self.service, self.factory, self.manager = object_impl(self.common, 7, [])

    def test_quaff_healing_and_poison(self):
        self.service.factory.utils_data(5)
        self.service.factory.common.impl_common(
            ObjectDummyService("!", "healing potion", "potion", 6)
        )
        self.service.helper_executor("q")
        self.assertEqual(len(self.service.factory.common.factory), 0)
        self.assertGreater(self.service.factory.helper, 0)
        self.service.factory.common.impl_common(
            ObjectDummyService("!", "poison", "potion", -4)
        )
        before = self.service.factory.helper
        self.service.helper_executor("q")
        self.assertEqual(self.service.factory.helper, before - 4)

    def test_quaff_with_two_potions_asks_which_one(self):
        game, _, _ = object_impl(self.common, 7, ["a"])
        game.factory.common.impl_common(
            ObjectDummyService("!", "healing potion", "potion", 6)
        )
        game.factory.common.impl_common(
            ObjectDummyService("!", "greater healing potion", "potion", 12)
        )
        game.factory.utils_data(10)
        game.helper_executor("q")
        self.assertEqual(len(game.factory.common.factory), 1)
        self.assertEqual(game.factory.common.factory[0].helper, 12)

    def test_scroll_of_mapping_reveals_the_whole_level(self):
        level = self.service.business.helper_i()
        self.service.factory.common.impl_common(
            ObjectDummyService("?", "scroll of magic mapping", "scroll", 0)
        )
        self.service.helper_executor("r")
        floor = sum(
            1
            for yy in range(level.executor.default)
            for xx in range(level.executor.common)
            if level.impl_dummy((xx, yy))
        )
        self.assertEqual(len(level.object.service), floor)

    def test_scroll_of_teleportation_moves_player(self):
        old = self.service.factory.data
        self.service.factory.common.impl_common(
            ObjectDummyService("?", "scroll of teleportation", "scroll", 0)
        )
        self.service.helper_executor("r")
        self.assertNotEqual(self.service.factory.data, old)

    def test_scroll_of_fireball_burns_visible_monsters(self):
        target = dummy_helper(self.service)[1]
        level = self.service.business.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.common, "D", target)
        level.object.factory[target] = monster
        self.service.impl_business()
        self.service.factory.common.impl_common(
            ObjectDummyService("?", "scroll of fireball", "scroll", 8)
        )
        self.service.helper_executor("r")
        self.assertIn(target, level.object.factory)
        self.assertLess(monster.helper, monster.factory)

    def test_scroll_of_fireball_kills_weak_monsters_for_xp(self):
        target = dummy_helper(self.service)[1]
        level = self.service.business.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.common, "r", target)
        level.object.factory[target] = monster
        self.service.impl_business()
        self.service.factory.common.impl_common(
            ObjectDummyService("?", "scroll of fireball", "scroll", 8)
        )
        self.service.helper_executor("r")
        self.assertNotIn(target, level.object.factory)
        self.assertGreater(self.service.factory.abstract, 0)

    def test_zap_wand_consumes_a_charge(self):
        game, _, _ = object_impl(self.common, 7, ["l"])
        wand = ObjectDummyService("/", "wand of magic missile", "wand", 5, 2)
        game.factory.common.impl_common(wand)
        game.helper_executor("z")
        self.assertEqual(wand.factory, 1)

    def test_zap_drained_wand_reports(self):
        game, _, _ = object_impl(self.common, 7, [])
        game.factory.common.impl_common(
            ObjectDummyService("/", "wand of magic missile", "wand", 5, 0)
        )
        game.helper_executor("z")
        self.assertIn("drained", game.abstract.service)

    def test_zap_with_bad_direction_never_minds(self):
        game, _, _ = object_impl(self.common, 7, ["x"])
        game.factory.common.impl_common(
            ObjectDummyService("/", "wand of magic missile", "wand", 5, 2)
        )
        game.helper_executor("z")
        self.assertIn("Never mind", game.abstract.service)

    def test_zap_bolt_can_kill_a_monster(self):
        game, _, _ = object_impl(self.common, 7, ["l", "l", "l", "l", "l"])
        level = game.business.helper_i()
        start = game.factory.data
        level.helper_executor((start[0] + 1, start[1]), ".")
        target = (start[0] + 2, start[1])
        level.helper_executor(target, ".")
        monster = AbstractBusinessFactory.builder_factory(self.common, "r", target)
        level.object.factory[target] = monster
        game.impl_business()
        game.factory.common.impl_common(
            ObjectDummyService("/", "wand of magic missile", "wand", 5, 5)
        )
        for _ in range(5):
            if not monster.i_object:
                break
            game.helper_executor("z")
        self.assertFalse(monster.i_object)
        self.assertGreater(game.factory.abstract, 0)

    def test_choose_invalid_letter_never_minds(self):
        game, _, _ = object_impl(self.common, 7, ["z"])
        game.factory.common.impl_common(
            ObjectDummyService("!", "healing potion", "potion", 6)
        )
        game.factory.common.impl_common(
            ObjectDummyService("!", "greater healing potion", "potion", 12)
        )
        game.helper_executor("q")
        self.assertIn("Never mind", game.abstract.service)
        self.assertEqual(len(game.factory.common.factory), 2)

    def test_i_business_ignores_unknown_command(self):
        self.service.i_business("x")
        self.assertIn("Welcome", self.service.abstract.service)

    def test_wield_and_wear_change_bonuses(self):
        before = self.service.factory.builder_utils()
        self.service.factory.common.impl_common(
            ObjectDummyService(")", "battle axe", "weapon", 3)
        )
        self.service.helper_executor("w")
        self.assertEqual(self.service.factory.builder_utils(), before + 3)
        before_def = self.service.factory.common_builder()
        self.service.factory.common.impl_common(
            ObjectDummyService("[", "chain mail", "armour", 2)
        )
        self.service.helper_executor("W")
        self.assertEqual(self.service.factory.common_builder(), before_def + 2)

    def test_inventory_help_unknown_save_and_quit(self):
        self.service.helper_executor("i")
        self.assertIn("Inventory", self.service.abstract.service)
        self.service.helper_executor("?")
        self.assertIn("hjkl", self.service.abstract.service)
        self.service.helper_executor("x")
        self.assertIn("Unknown key", self.service.abstract.service)
        self.service.helper_executor("s")
        self.assertEqual(len(self.manager), 1)
        self.assertEqual(self.service.abstract.service, "Game saved.")
        self.service.helper_executor("Q")
        self.assertTrue(self.service.abstract.data)
        self.service.helper_executor("")
        self.assertTrue(self.service.abstract.data)


class TestFlow(unittest.TestCase):
    def setUp(self):
        self.common = utils_common()
        self.service, self.factory, self.manager = object_impl(self.common, 7, [])

    def test_descend_and_ascend(self):
        level = self.service.business.helper_i()
        self.service.factory.data = level.processor
        self.service.helper_executor(">")
        self.assertEqual(self.service.business.data, 2)
        self.assertIn(2, self.service.business.factory)
        level2 = self.service.business.helper_i()
        self.assertEqual(self.service.factory.data, level2.manager[0].utils_common)
        self.assertEqual(self.service.abstract.service, helper_arolla(2))
        self.service.factory.data = level2.manager[0].utils_common
        self.service.helper_executor("<")
        self.assertEqual(self.service.abstract.service, "No stairs up here.")
        self.service.business.i_impl(self.common, 1)
        level1 = self.service.business.helper_i()
        self.service.factory.data = level1.utils
        self.service.helper_executor("<")
        self.assertIn("sealed", self.service.abstract.service)
        self.service.factory.common.impl_common(object_arolla(self.common))
        self.service.helper_executor("<")
        self.assertTrue(self.service.abstract.helper)
        self.assertTrue(self.service.abstract.data)
        self.assertEqual(self.service.abstract.service, impl_common("win"))

    def test_adjacent_visible_monster_attacks_on_rest(self):
        target = dummy_helper(self.service)[1]
        level = self.service.business.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.common, "o", target)
        level.object.factory[target] = monster
        self.service.impl_business()
        before = self.service.factory.helper
        self.service.helper_executor(".")
        self.assertLessEqual(self.service.factory.helper, before)
        self.assertIn("orc", self.service.abstract.service)

    def test_player_death_ends_the_game(self):
        target = dummy_helper(self.service)[1]
        level = self.service.business.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.common, "T", target)
        level.object.factory[target] = monster
        self.service.impl_business()
        self.service.factory.helper = 1
        for _ in range(10):
            if self.service.abstract.data:
                break
            self.service.helper_executor(".")
        self.assertTrue(self.service.abstract.data)
        self.assertEqual(self.service.abstract.service, impl_common("death"))

    def test_play_loop_renders_and_quits(self):
        game, written, _ = object_impl(self.common, 7, ["h", "Q"])
        game.arolla_service()
        self.assertTrue(game.abstract.data)
        self.assertGreaterEqual(len(written), 2)
        self.assertTrue(written[0].startswith("\x1b[2J\x1b[H"))

    def test_to_dict_and_from_dict_round_trip(self):
        config = utils_common()
        game, _, _ = object_impl(config, 7, [])
        game.helper_executor("h")
        game.impl_business()
        stream = iter([""] * 5)
        io = ArollaBusinessFactory(stream.__next__, lambda impl: None, lambda service: None)
        clone = ManagerIExecutor.dummy_manager(config, io, game.executor_arolla())
        self.assertEqual(clone.executor_arolla(), game.executor_arolla())


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.common = utils_common()
        self.service, self.factory, self.manager = object_impl(self.common, 7, [])

    def test_empty_inventory_commands_report_missing_item(self):
        pairs = (("q", "potion"), ("r", "scroll"), ("w", "weapon"), ("W", "armour"), ("z", "wand"))
        for key, word in pairs:
            self.service.helper_executor(key)
            self.assertIn(f"No {word}", self.service.abstract.service)

    def test_zap_into_wall_with_last_charge_crumbles_wand(self):
        game, _, _ = object_impl(self.common, 7, ["h"])
        level = game.business.helper_i()
        level.helper_executor((1, 1), ".")
        game.factory.data = (1, 1)
        wand = ObjectDummyService("/", "wand of magic missile", "wand", 5, 1)
        game.factory.common.impl_common(wand)
        game.helper_executor("z")
        self.assertIn("fizzles", game.abstract.service)
        self.assertIn("crumbles", game.abstract.service)
        self.assertNotIn(wand, game.factory.common.factory)

    def test_zap_bolt_hits_monster_in_line(self):
        game, _, _ = object_impl(self.common, 7, ["l"])
        level = game.business.helper_i()
        start = game.factory.data
        level.helper_executor((start[0] + 1, start[1]), ".")
        target = (start[0] + 2, start[1])
        level.helper_executor(target, ".")
        monster = AbstractBusinessFactory.builder_factory(self.common, "D", target)
        level.object.factory[target] = monster
        game.factory.common.impl_common(
            ObjectDummyService("/", "wand of magic missile", "wand", 5, 3)
        )
        game.helper_executor("z")
        self.assertIn("bolt hits", game.abstract.service)
        self.assertLess(monster.helper, monster.factory)

    def test_inventory_text_lists_gear_and_items(self):
        self.service.factory.common.impl_common(
            ObjectDummyService("!", "healing potion", "potion", 6)
        )
        self.service.factory.common.utils_i(ObjectDummyService(")", "dagger", "weapon", 1))
        self.service.factory.common.executor_i(
            ObjectDummyService("[", "leather armour", "armour", 1)
        )
        self.service.helper_executor("i")
        self.assertIn("Inventory:", self.service.abstract.service)
        self.assertIn("wielding dagger", self.service.abstract.service)
        self.assertIn("wearing leather armour", self.service.abstract.service)

    def test_descend_without_stairs_reports(self):
        self.service.helper_executor(">")
        self.assertEqual(self.service.abstract.service, "No stairs down here.")

    def test_ascend_from_deeper_level_climbs_up(self):
        level = self.service.business.helper_i()
        self.service.factory.data = level.processor
        self.service.helper_executor(">")
        level2 = self.service.business.helper_i()
        self.service.factory.data = level2.utils
        self.service.helper_executor("<")
        self.assertEqual(self.service.business.data, 1)
        self.assertIn("climb up to depth 1", self.service.abstract.service)

    def test_attack_can_miss_against_high_defence(self):
        config = abstract_business(
            "monster r tank rat 3 2 1000 2 1\nitem gold $ pile 0\ntrap dart\n"
        )
        game, _, _ = object_impl(config, 7, [])
        key, target = dummy_helper(game)
        level = game.business.helper_i()
        monster = AbstractBusinessFactory.builder_factory(config, "r", target)
        level.object.factory[target] = monster
        game.impl_business()
        messages = set()
        for _ in range(5):
            game.helper_executor(key)
            messages.add(game.abstract.service)
        self.assertTrue(any("miss" in message for message in messages))

    def test_hit_without_kill_reports_damage(self):
        key, target = dummy_helper(self.service)
        level = self.service.business.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.common, "D", target)
        level.object.factory[target] = monster
        self.service.impl_business()
        messages = set()
        for _ in range(5):
            self.service.helper_executor(key)
            messages.add(self.service.abstract.service)
        self.assertIn(target, level.object.factory)
        self.assertLess(monster.helper, monster.factory)


if __name__ == "__main__":
    unittest.main()
