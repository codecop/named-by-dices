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


def object_impl(config, seed, keys):
    stream = iter(list(keys) + [""] * 50)
    written = []
    saved = []
    io = ArollaBusinessFactory(stream.__next__, written.append, saved.append)
    game = ManagerIExecutor(config, seed, io)
    return game, written, saved


def free_neighbour(game):
    level = game.world.helper_i()
    start = game.player.data
    for key, delta in UTILS_DEFAULT.items():
        target = (start[0] + delta[0], start[1] + delta[1])
        if level.impl_dummy(target) and target not in level.object.factory:
            return key, target
    raise AssertionError("no free neighbour")


class TestNewGame(unittest.TestCase):
    def test_new_game_has_level_player_monsters_npc_and_items(self):
        config = utils_common()
        game, _, _ = object_impl(config, 7, [])
        level = game.world.helper_i()
        self.assertEqual(game.world.data, 1)
        self.assertGreaterEqual(len(level.manager), config.helper.factory)
        self.assertEqual(game.player.data, level.manager[0].utils_common)
        self.assertTrue(level.object.factory)
        self.assertTrue(any(m.processor for m in level.object.factory.values()))
        self.assertTrue(level.object.helper)
        game.impl_business()
        self.assertTrue(game.visible)

    def test_deepest_level_gets_artefact_and_boss(self):
        config = utils_common()
        level = data_service(config, random.Random(3), config.helper.data)
        default_service(config, level, random.Random(4), config.helper.data)
        kinds = [item.data for item in level.object.helper.values()]
        self.assertIn("artefact", kinds)
        self.assertTrue(any(m.impl == "D" for m in level.object.factory.values()))


class TestMovement(unittest.TestCase):
    def setUp(self):
        self.config = utils_common()
        self.game, self.written, self.saved = object_impl(self.config, 7, [])

    def test_move_into_wall_keeps_position(self):
        self.game.player.data = (0, 0)
        self.game.handle("l")
        self.assertEqual(self.game.player.data, (0, 0))
        self.assertEqual(self.game.status.service, "A wall.")

    def test_move_onto_floor_moves_player(self):
        key, target = free_neighbour(self.game)
        self.game.handle(key)
        self.assertEqual(self.game.player.data, target)

    def test_attack_kills_monster_and_grants_xp(self):
        key, target = free_neighbour(self.game)
        level = self.game.world.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.config, "r", target)
        level.object.factory[target] = monster
        for _ in range(10):
            self.game.handle(key)
            if target not in level.object.factory:
                break
        self.assertNotIn(target, level.object.factory)
        self.assertGreater(self.game.player.abstract, 0)

    def test_friendly_npc_heals_once_then_gives_advice(self):
        key, target = free_neighbour(self.game)
        level = self.game.world.helper_i()
        npc = AbstractBusinessFactory.builder_factory(self.config, "H", target)
        level.object.factory[target] = npc
        self.game.player.helper = 1
        self.game.handle(key)
        self.assertEqual(self.game.player.helper, self.game.player.factory)
        self.assertTrue(npc.utils)
        self.game.handle(key)
        self.assertIn("Golden Die", self.game.status.service)

    def test_pickup_item_gold_and_artefact(self):
        level = self.game.world.helper_i()
        pos = self.game.player.data
        level.object.helper[pos] = ObjectDummyService("!", "healing potion", "potion", 6)
        self.game.handle(",")
        self.assertEqual(len(self.game.player.common.factory), 1)
        self.assertNotIn(pos, level.object.helper)
        level.object.helper[pos] = ObjectDummyService("$", "pile of gold", "gold", 30)
        self.game.handle(",")
        self.assertEqual(self.game.player.common.service, 30)
        level.object.helper[pos] = object_arolla(self.config)
        self.game.handle(",")
        self.assertEqual(self.game.status.service, impl_common("amulet"))
        self.game.handle(",")
        self.assertEqual(self.game.status.service, "Nothing here.")

    def test_teleport_trap_moves_player_and_is_found(self):
        key, target = free_neighbour(self.game)
        level = self.game.world.helper_i()
        old = self.game.player.data
        level.object.impl[target] = ImplProcessorDefault("teleport")
        self.game.handle(key)
        self.assertTrue(level.object.impl[target].helper)
        self.assertNotEqual(self.game.player.data, old)
        self.assertIn("teleport", self.game.status.service)

    def test_dart_trap_damages_player(self):
        target = free_neighbour(self.game)[1]
        key = free_neighbour(self.game)[0]
        level = self.game.world.helper_i()
        level.object.impl[target] = ImplProcessorDefault("dart")
        before = self.game.player.helper
        self.game.handle(key)
        self.assertTrue(level.object.impl[target].helper)
        self.assertLessEqual(self.game.player.helper, before)

    def test_alarm_trap_spawns_monsters(self):
        key, target = free_neighbour(self.game)
        level = self.game.world.helper_i()
        before = len(level.object.factory)
        level.object.impl[target] = ImplProcessorDefault("alarm")
        self.game.handle(key)
        self.assertEqual(len(level.object.factory), before + 2)


class TestItems(unittest.TestCase):
    def setUp(self):
        self.config = utils_common()
        self.game, self.written, self.saved = object_impl(self.config, 7, [])

    def test_quaff_healing_and_poison(self):
        self.game.player.utils_data(5)
        self.game.player.common.impl_common(
            ObjectDummyService("!", "healing potion", "potion", 6)
        )
        self.game.handle("q")
        self.assertEqual(len(self.game.player.common.factory), 0)
        self.assertGreater(self.game.player.helper, 0)
        self.game.player.common.impl_common(
            ObjectDummyService("!", "poison", "potion", -4)
        )
        before = self.game.player.helper
        self.game.handle("q")
        self.assertEqual(self.game.player.helper, before - 4)

    def test_quaff_with_two_potions_asks_which_one(self):
        game, _, _ = object_impl(self.config, 7, ["a"])
        game.player.common.impl_common(
            ObjectDummyService("!", "healing potion", "potion", 6)
        )
        game.player.common.impl_common(
            ObjectDummyService("!", "greater healing potion", "potion", 12)
        )
        game.player.utils_data(10)
        game.handle("q")
        self.assertEqual(len(game.player.common.factory), 1)
        self.assertEqual(game.player.common.factory[0].helper, 12)

    def test_scroll_of_mapping_reveals_the_whole_level(self):
        level = self.game.world.helper_i()
        self.game.player.common.impl_common(
            ObjectDummyService("?", "scroll of magic mapping", "scroll", 0)
        )
        self.game.handle("r")
        floor = sum(
            1
            for yy in range(level.executor.default)
            for xx in range(level.executor.common)
            if level.impl_dummy((xx, yy))
        )
        self.assertEqual(len(level.object.service), floor)

    def test_scroll_of_teleportation_moves_player(self):
        old = self.game.player.data
        self.game.player.common.impl_common(
            ObjectDummyService("?", "scroll of teleportation", "scroll", 0)
        )
        self.game.handle("r")
        self.assertNotEqual(self.game.player.data, old)

    def test_scroll_of_fireball_burns_visible_monsters(self):
        target = free_neighbour(self.game)[1]
        level = self.game.world.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.config, "D", target)
        level.object.factory[target] = monster
        self.game.impl_business()
        self.game.player.common.impl_common(
            ObjectDummyService("?", "scroll of fireball", "scroll", 8)
        )
        self.game.handle("r")
        self.assertIn(target, level.object.factory)
        self.assertLess(monster.helper, monster.factory)

    def test_scroll_of_fireball_kills_weak_monsters_for_xp(self):
        target = free_neighbour(self.game)[1]
        level = self.game.world.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.config, "r", target)
        level.object.factory[target] = monster
        self.game.impl_business()
        self.game.player.common.impl_common(
            ObjectDummyService("?", "scroll of fireball", "scroll", 8)
        )
        self.game.handle("r")
        self.assertNotIn(target, level.object.factory)
        self.assertGreater(self.game.player.abstract, 0)

    def test_zap_wand_consumes_a_charge(self):
        game, _, _ = object_impl(self.config, 7, ["l"])
        wand = ObjectDummyService("/", "wand of magic missile", "wand", 5, 2)
        game.player.common.impl_common(wand)
        game.handle("z")
        self.assertEqual(wand.factory, 1)

    def test_zap_drained_wand_reports(self):
        game, _, _ = object_impl(self.config, 7, [])
        game.player.common.impl_common(
            ObjectDummyService("/", "wand of magic missile", "wand", 5, 0)
        )
        game.handle("z")
        self.assertIn("drained", game.status.service)

    def test_zap_with_bad_direction_never_minds(self):
        game, _, _ = object_impl(self.config, 7, ["x"])
        game.player.common.impl_common(
            ObjectDummyService("/", "wand of magic missile", "wand", 5, 2)
        )
        game.handle("z")
        self.assertIn("Never mind", game.status.service)

    def test_zap_bolt_can_kill_a_monster(self):
        game, _, _ = object_impl(self.config, 7, ["l", "l", "l", "l", "l"])
        level = game.world.helper_i()
        start = game.player.data
        level.helper_executor((start[0] + 1, start[1]), ".")
        target = (start[0] + 2, start[1])
        level.helper_executor(target, ".")
        monster = AbstractBusinessFactory.builder_factory(self.config, "r", target)
        level.object.factory[target] = monster
        game.impl_business()
        game.player.common.impl_common(
            ObjectDummyService("/", "wand of magic missile", "wand", 5, 5)
        )
        for _ in range(5):
            if not monster.i_object:
                break
            game.handle("z")
        self.assertFalse(monster.i_object)
        self.assertGreater(game.player.abstract, 0)

    def test_choose_invalid_letter_never_minds(self):
        game, _, _ = object_impl(self.config, 7, ["z"])
        game.player.common.impl_common(
            ObjectDummyService("!", "healing potion", "potion", 6)
        )
        game.player.common.impl_common(
            ObjectDummyService("!", "greater healing potion", "potion", 12)
        )
        game.handle("q")
        self.assertIn("Never mind", game.status.service)
        self.assertEqual(len(game.player.common.factory), 2)

    def test_i_business_ignores_unknown_command(self):
        self.game.i_business("x")
        self.assertIn("Welcome", self.game.status.service)

    def test_wield_and_wear_change_bonuses(self):
        before = self.game.player.builder_utils()
        self.game.player.common.impl_common(
            ObjectDummyService(")", "battle axe", "weapon", 3)
        )
        self.game.handle("w")
        self.assertEqual(self.game.player.builder_utils(), before + 3)
        before_def = self.game.player.common_builder()
        self.game.player.common.impl_common(
            ObjectDummyService("[", "chain mail", "armour", 2)
        )
        self.game.handle("W")
        self.assertEqual(self.game.player.common_builder(), before_def + 2)

    def test_inventory_help_unknown_save_and_quit(self):
        self.game.handle("i")
        self.assertIn("Inventory", self.game.status.service)
        self.game.handle("?")
        self.assertIn("hjkl", self.game.status.service)
        self.game.handle("x")
        self.assertIn("Unknown key", self.game.status.service)
        self.game.handle("s")
        self.assertEqual(len(self.saved), 1)
        self.assertEqual(self.game.status.service, "Game saved.")
        self.game.handle("Q")
        self.assertTrue(self.game.status.data)
        self.game.handle("")
        self.assertTrue(self.game.status.data)


class TestFlow(unittest.TestCase):
    def setUp(self):
        self.config = utils_common()
        self.game, self.written, self.saved = object_impl(self.config, 7, [])

    def test_descend_and_ascend(self):
        level = self.game.world.helper_i()
        self.game.player.data = level.processor
        self.game.handle(">")
        self.assertEqual(self.game.world.data, 2)
        self.assertIn(2, self.game.world.factory)
        level2 = self.game.world.helper_i()
        self.assertEqual(self.game.player.data, level2.manager[0].utils_common)
        self.assertEqual(self.game.status.service, helper_arolla(2))
        self.game.player.data = level2.manager[0].utils_common
        self.game.handle("<")
        self.assertEqual(self.game.status.service, "No stairs up here.")
        self.game.world.i_impl(self.config, 1)
        level1 = self.game.world.helper_i()
        self.game.player.data = level1.utils
        self.game.handle("<")
        self.assertIn("sealed", self.game.status.service)
        self.game.player.common.impl_common(object_arolla(self.config))
        self.game.handle("<")
        self.assertTrue(self.game.status.helper)
        self.assertTrue(self.game.status.data)
        self.assertEqual(self.game.status.service, impl_common("win"))

    def test_adjacent_visible_monster_attacks_on_rest(self):
        target = free_neighbour(self.game)[1]
        level = self.game.world.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.config, "o", target)
        level.object.factory[target] = monster
        self.game.impl_business()
        before = self.game.player.helper
        self.game.handle(".")
        self.assertLessEqual(self.game.player.helper, before)
        self.assertIn("orc", self.game.status.service)

    def test_player_death_ends_the_game(self):
        target = free_neighbour(self.game)[1]
        level = self.game.world.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.config, "T", target)
        level.object.factory[target] = monster
        self.game.impl_business()
        self.game.player.helper = 1
        for _ in range(10):
            if self.game.status.data:
                break
            self.game.handle(".")
        self.assertTrue(self.game.status.data)
        self.assertEqual(self.game.status.service, impl_common("death"))

    def test_play_loop_renders_and_quits(self):
        game, written, _ = object_impl(self.config, 7, ["h", "Q"])
        game.play()
        self.assertTrue(game.status.data)
        self.assertGreaterEqual(len(written), 2)
        self.assertTrue(written[0].startswith("\x1b[2J\x1b[H"))

    def test_to_dict_and_from_dict_round_trip(self):
        config = utils_common()
        game, _, _ = object_impl(config, 7, [])
        game.handle("h")
        game.impl_business()
        stream = iter([""] * 5)
        io = ArollaBusinessFactory(stream.__next__, lambda text: None, lambda g: None)
        clone = ManagerIExecutor.dummy_manager(config, io, game.executor_arolla())
        self.assertEqual(clone.executor_arolla(), game.executor_arolla())


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.config = utils_common()
        self.game, self.written, self.saved = object_impl(self.config, 7, [])

    def test_empty_inventory_commands_report_missing_item(self):
        pairs = (("q", "potion"), ("r", "scroll"), ("w", "weapon"), ("W", "armour"), ("z", "wand"))
        for key, word in pairs:
            self.game.handle(key)
            self.assertIn(f"No {word}", self.game.status.service)

    def test_zap_into_wall_with_last_charge_crumbles_wand(self):
        game, _, _ = object_impl(self.config, 7, ["h"])
        level = game.world.helper_i()
        level.helper_executor((1, 1), ".")
        game.player.data = (1, 1)
        wand = ObjectDummyService("/", "wand of magic missile", "wand", 5, 1)
        game.player.common.impl_common(wand)
        game.handle("z")
        self.assertIn("fizzles", game.status.service)
        self.assertIn("crumbles", game.status.service)
        self.assertNotIn(wand, game.player.common.factory)

    def test_zap_bolt_hits_monster_in_line(self):
        game, _, _ = object_impl(self.config, 7, ["l"])
        level = game.world.helper_i()
        start = game.player.data
        level.helper_executor((start[0] + 1, start[1]), ".")
        target = (start[0] + 2, start[1])
        level.helper_executor(target, ".")
        monster = AbstractBusinessFactory.builder_factory(self.config, "D", target)
        level.object.factory[target] = monster
        game.player.common.impl_common(
            ObjectDummyService("/", "wand of magic missile", "wand", 5, 3)
        )
        game.handle("z")
        self.assertIn("bolt hits", game.status.service)
        self.assertLess(monster.helper, monster.factory)

    def test_inventory_text_lists_gear_and_items(self):
        self.game.player.common.impl_common(
            ObjectDummyService("!", "healing potion", "potion", 6)
        )
        self.game.player.common.utils_i(ObjectDummyService(")", "dagger", "weapon", 1))
        self.game.player.common.executor_i(
            ObjectDummyService("[", "leather armour", "armour", 1)
        )
        self.game.handle("i")
        self.assertIn("Inventory:", self.game.status.service)
        self.assertIn("wielding dagger", self.game.status.service)
        self.assertIn("wearing leather armour", self.game.status.service)

    def test_descend_without_stairs_reports(self):
        self.game.handle(">")
        self.assertEqual(self.game.status.service, "No stairs down here.")

    def test_ascend_from_deeper_level_climbs_up(self):
        level = self.game.world.helper_i()
        self.game.player.data = level.processor
        self.game.handle(">")
        level2 = self.game.world.helper_i()
        self.game.player.data = level2.utils
        self.game.handle("<")
        self.assertEqual(self.game.world.data, 1)
        self.assertIn("climb up to depth 1", self.game.status.service)

    def test_attack_can_miss_against_high_defence(self):
        config = abstract_business(
            "monster r tank rat 3 2 1000 2 1\nitem gold $ pile 0\ntrap dart\n"
        )
        game, _, _ = object_impl(config, 7, [])
        key, target = free_neighbour(game)
        level = game.world.helper_i()
        monster = AbstractBusinessFactory.builder_factory(config, "r", target)
        level.object.factory[target] = monster
        game.impl_business()
        messages = set()
        for _ in range(5):
            game.handle(key)
            messages.add(game.status.service)
        self.assertTrue(any("miss" in message for message in messages))

    def test_hit_without_kill_reports_damage(self):
        key, target = free_neighbour(self.game)
        level = self.game.world.helper_i()
        monster = AbstractBusinessFactory.builder_factory(self.config, "D", target)
        level.object.factory[target] = monster
        self.game.impl_business()
        messages = set()
        for _ in range(5):
            self.game.handle(key)
            messages.add(self.game.status.service)
        self.assertIn(target, level.object.factory)
        self.assertLess(monster.helper, monster.factory)


if __name__ == "__main__":
    unittest.main()
