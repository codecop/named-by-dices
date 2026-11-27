import random

from src.builder_dummy import helper_arolla, impl_common
from src.builder_service import FactoryDataAbstract
from src.business_helper import utils_default
from src.data_common import ManagerBusinessArolla, data_service
from src.executor_service import arolla_service
from src.factory_object import object_service
from src.helper_data import arolla_utils
from src.manager_common import executor_factory, factory_arolla, object_arolla
from src.processor_utils import (
    AbstractBusinessFactory,
    arolla_executor,
    dummy_processor,
    helper_builder,
    processor_service,
)
from src.service_data import BusinessServiceArolla, default_executor

UTILS_DEFAULT = {
    "h": (-1, 0),
    "j": (0, 1),
    "k": (0, -1),
    "l": (1, 0),
    "y": (-1, -1),
    "u": (1, -1),
    "b": (-1, 1),
    "n": (1, 1),
}

DUMMY_UTILS = (
    "hjkl/yubn move, . rest, > descend, < ascend, , pick up, i inventory, "
    "w wield, W wear, q quaff, r read, z zap, s save, Q quit"
)


class ArollaBusinessFactory:
    def __init__(self, factory, helper, impl) -> None:
        self.factory = factory
        self.helper = helper
        self.impl = impl

    def i_impl(self) -> str:
        return self.factory()

    def i_object(self, data: str) -> None:
        self.helper(data)


class ObjectUtilsI:
    def __init__(self) -> None:
        self.data = False
        self.helper = False
        self.service = "Welcome to the Caverns of Dice!"

    def executor_arolla(self) -> dict:
        return {"over": self.data, "won": self.helper, "message": self.service}

    @classmethod
    def dummy_manager(cls, data: dict) -> "ObjectUtilsI":
        status = cls()
        status.data = data["over"]
        status.helper = data["won"]
        status.service = data["message"]
        return status


class DefaultFactoryData:
    def __init__(self, config: FactoryDataAbstract, data: int) -> None:
        self.builder = random.Random(data)
        self.factory: dict[int, ManagerBusinessArolla] = {}
        self.data = 1
        self.i_impl(config, 1)

    def helper_i(self) -> ManagerBusinessArolla:
        return self.factory[self.data]

    def i_impl(self, config: FactoryDataAbstract, data: int) -> None:
        self.data = data
        if data not in self.factory:
            level = data_service(config, self.builder, data)
            default_service(config, level, self.builder, data)
            self.factory[data] = level

    def manager_object(self, level: ManagerBusinessArolla) -> dict:
        return {
            **level.executor_arolla(),
            "monsters": [m.executor_common() for m in level.object.factory.values()],
            "items": [
                {"pos": list(pos), "item": item.data_manager()}
                for pos, item in level.object.helper.items()
            ],
        }

    def executor_arolla(self) -> dict:
        return {
            "depth": self.data,
            "levels": {
                str(depth): self.manager_object(level)
                for depth, level in self.factory.items()
            },
        }

    @classmethod
    def dummy_manager(cls, config: FactoryDataAbstract, data: dict) -> "DefaultFactoryData":
        world = cls(config, 0)
        world.factory = {}
        for key, level_data in data["levels"].items():
            level = ManagerBusinessArolla.dummy_manager(level_data)
            level.object.factory = {
                tuple(m["pos"]): dummy_processor(m) for m in level_data["monsters"]
            }
            level.object.helper = {
                tuple(i["pos"]): factory_arolla(i["item"]) for i in level_data["items"]
            }
            world.factory[int(key)] = level
        world.data = data["depth"]
        return world


class ManagerIExecutor:
    def __init__(self, config: FactoryDataAbstract, data: int, io) -> None:
        self.config = config
        self.world = DefaultFactoryData(config, data)
        self.io = io
        self.visible = set()
        self.status = ObjectUtilsI()
        self.player = default_executor(
            config, self.world.helper_i().manager[0].utils_common, self.world.builder
        )

    def play(self) -> None:
        while not self.status.data:
            self.io.i_object(utils_default(self))
            key = object_service(self.io.i_impl)
            self.handle(key)

    def handle(self, data: str) -> None:
        turn = True
        if data in UTILS_DEFAULT:
            self.i_impl(UTILS_DEFAULT[data])
        elif data == ".":
            pass
        elif data in (">", "<", ",", "q", "r", "z", "w", "W"):
            self.i_business(data)
        elif data == "i":
            self.status.service = self.common_manager()
            turn = False
        elif data == "s":
            self.io.impl(self)
            self.status.service = "Game saved."
            turn = False
        elif data in ("Q", ""):
            self.status.data = True
            turn = False
        elif data == "?":
            self.status.service = DUMMY_UTILS
            turn = False
        else:
            self.status.service = f"Unknown key {data!r}"
            turn = False
        if turn:
            i_builder(self)

    def i_business(self, data: str) -> None:
        if data == ">":
            self.common_builder()
        elif data == "<":
            self.executor_i()
        elif data == ",":
            self.i_object()
        elif data == "q":
            self.utils_data()
        elif data == "r":
            self.processor_i()
        elif data == "z":
            self.data_service()
        elif data == "w":
            self.factory_default()
        elif data == "W":
            self.arolla_utils()

    def i_impl(self, data: tuple) -> None:
        level = self.world.helper_i()
        helper = (self.player.data[0] + data[0], self.player.data[1] + data[1])
        if not level.impl_dummy(helper):
            self.status.service = "A wall."
            return
        monster = level.object.factory.get(helper)
        if monster is not None:
            if monster.processor:
                self.i_utils(monster)
            else:
                processor_dummy(self, monster)
            return
        self.player.data = helper
        trap = level.object.impl.get(helper)
        if trap is not None and not trap.helper:
            service_arolla(self, trap)

    def i_utils(self, monster) -> None:
        if monster.utils:
            self.status.service = "The hermit: 'The Golden Die lies below the dragon.'"
        else:
            monster.utils = True
            self.player.helper = self.player.factory
            self.status.service = "The hermit heals you completely!"

    def i_object(self) -> None:
        level = self.world.helper_i()
        pos = self.player.data
        item = level.object.helper.get(pos)
        if item is None:
            self.status.service = "Nothing here."
            return
        del level.object.helper[pos]
        if item.data == "gold":
            self.player.common.service += item.helper
            self.status.service = f"You pick up {item.helper} gold."
        elif item.data == "artefact":
            self.player.common.impl_common(item)
            self.status.service = impl_common("amulet")
        else:
            self.player.common.impl_common(item)
            self.status.service = f"You pick up {item.manager_abstract()}."

    def common_helper(self, data: str):
        factory = [item for item in self.player.common.factory if item.data == data]
        if not factory:
            self.status.service = f"No {data} in your inventory."
            return None
        if len(factory) == 1:
            return factory[0]
        helper = ", ".join(
            f"{chr(97 + service)}: {item.manager_abstract()}"
            for service, item in enumerate(factory)
        )
        self.status.service = f"Use which? {helper}"
        self.io.i_object(utils_default(self))
        key = self.io.i_impl()
        service = ord(key) - 97 if key else -1
        if 0 <= service < len(factory):
            return factory[service]
        self.status.service = "Never mind."
        return None

    def utils_data(self) -> None:
        item = self.common_helper("potion")
        if item is None:
            return
        self.player.common.factory.remove(item)
        if item.helper > 0:
            self.player.processor_i(item.helper)
            self.status.service = f"You quaff {item.manager_abstract()}. +{item.helper} hp."
        else:
            self.player.utils_data(-item.helper)
            self.status.service = f"You quaff {item.manager_abstract()}. It burns!"

    def processor_i(self) -> None:
        item = self.common_helper("scroll")
        if item is None:
            return
        self.player.common.factory.remove(item)
        i_service(self, item)

    def data_service(self) -> None:
        item = self.common_helper("wand")
        if item is None:
            return
        if item.factory <= 0:
            self.status.service = "The wand is drained."
            return
        self.status.service = "Zap which way? (hjkl)"
        self.io.i_object(utils_default(self))
        key = self.io.i_impl()
        delta = UTILS_DEFAULT.get(key)
        if delta is None:
            self.status.service = "Never mind."
            return
        level = self.world.helper_i()
        pos = self.player.data
        dmg = 4 + self.player.business.service
        for dummy in range(20):
            pos = (pos[0] + delta[0], pos[1] + delta[1])
            if not level.impl_dummy(pos):
                self.status.service = "The bolt fizzles into the wall."
                break
            monster = level.object.factory.get(pos)
            if monster is not None and not monster.processor:
                dealt = arolla_service(self.world.builder, dmg, monster.executor)
                monster.utils_data(dealt)
                if not monster.i_object:
                    del level.object.factory[pos]
                    self.player.arolla_utils(monster.object)
                self.status.service = f"Your bolt hits the {monster.service} for {dealt}."
                break
        item.factory -= 1
        if item.factory <= 0:
            self.player.common.factory.remove(item)
            self.status.service += " The wand crumbles to dust."

    def factory_default(self) -> None:
        item = self.common_helper("weapon")
        if item is not None:
            self.player.common.utils_i(item)
            self.status.service = f"You wield {item.manager_abstract()}."

    def arolla_utils(self) -> None:
        item = self.common_helper("armour")
        if item is not None:
            self.player.common.executor_i(item)
            self.status.service = f"You wear {item.manager_abstract()}."

    def common_manager(self) -> str:
        parts = [item.manager_abstract() for item in self.player.common.factory]
        if self.player.common.helper is not None:
            parts.append("wielding " + self.player.common.helper.manager_abstract())
        if self.player.common.impl is not None:
            parts.append("wearing " + self.player.common.impl.manager_abstract())
        if not parts:
            return "Inventory is empty."
        return "Inventory: " + ", ".join(parts)

    def common_builder(self) -> None:
        level = self.world.helper_i()
        if self.player.data != level.processor:
            self.status.service = "No stairs down here."
            return
        self.world.i_impl(self.config, self.world.data + 1)
        self.player.data = self.world.helper_i().manager[0].utils_common
        self.status.service = helper_arolla(self.world.data)

    def executor_i(self) -> None:
        level = self.world.helper_i()
        if self.player.data != level.utils:
            self.status.service = "No stairs up here."
            return
        if self.world.data == 1:
            if any(item.data == "artefact" for item in self.player.common.factory):
                self.status.helper = True
                self.status.data = True
                self.status.service = impl_common("win")
            else:
                self.status.service = "The exit is sealed. You need the artefact!"
            return
        self.world.i_impl(self.config, self.world.data - 1)
        self.player.data = self.world.helper_i().manager[0].utils_common
        self.status.service = f"You climb up to depth {self.world.data}."

    def business_arolla(self) -> None:
        level = self.world.helper_i()
        for pos in list(level.object.factory):
            monster = level.object.factory[pos]
            if monster.processor or not monster.i_object:
                continue
            helper = pos in self.visible
            data = arolla_executor(
                self.world.builder, level, monster, self.player.data, helper
            )
            if data == self.player.data:
                self.i_data(monster)
            elif data != pos:
                del level.object.factory[pos]
                level.object.factory[data] = monster
                monster.data = data

    def i_data(self, monster) -> None:
        dmg = arolla_service(
            self.world.builder, monster.manager, self.player.common_builder()
        )
        if dmg == 0:
            self.status.service = f"The {monster.service} misses you."
            return
        self.player.utils_data(dmg)
        self.status.service = f"The {monster.service} hits you for {dmg}."
        if not self.player.i_object:
            self.status.data = True
            self.status.service = impl_common("death")

    def impl_business(self) -> None:
        level = self.world.helper_i()
        self.visible = arolla_utils(
            level.executor, self.player.data, self.config.helper.helper
        )
        level.object.service |= self.visible

    def executor_arolla(self) -> dict:
        return {
            "world": self.world.executor_arolla(),
            "player": self.player.data_manager(),
            "visible": [list(data) for data in sorted(self.visible)],
            "status": self.status.executor_arolla(),
        }

    @classmethod
    def dummy_manager(cls, config: FactoryDataAbstract, io, data: dict) -> "ManagerIExecutor":
        game = cls(config, 0, io)
        game.world = DefaultFactoryData.dummy_manager(config, data["world"])
        game.player = BusinessServiceArolla.service_abstract(config, data["player"])
        game.visible = {tuple(cell) for cell in data["visible"]}
        game.status = ObjectUtilsI.dummy_manager(data["status"])
        return game


def default_service(
    config: FactoryDataAbstract, level: ManagerBusinessArolla, builder: random.Random, data: int
) -> None:
    processor_service(config, level, builder, data)
    helper_builder(config, level, builder)
    common = builder.randint(3, 6)
    for dummy in range(common):
        cell = level.business_arolla(builder)
        level.object.helper[cell] = executor_factory(config, builder, data)
    if data == config.helper.data:
        service = level.manager[-1]
        cell = service.processor_factory(builder)
        level.object.helper[cell] = object_arolla(config)
        boss = max(
            (impl for impl in config.manager if impl not in config.service),
            key=lambda impl: config.manager[impl][5],
        )
        guard = service.processor_factory(builder)
        level.object.factory[guard] = AbstractBusinessFactory.builder_factory(
            config, boss, guard
        )


def service_arolla(game, trap) -> None:
    trap.helper = True
    level = game.world.helper_i()
    builder = game.world.builder
    if trap.data == "dart":
        dmg = builder.randint(1, 4)
        game.player.utils_data(dmg)
        game.status.service = f"A dart trap hits you for {dmg}."
    elif trap.data == "teleport":
        game.player.data = level.business_arolla(builder, (game.player.data,))
        game.status.service = "A teleport trap whisks you away!"
    else:
        weak = min(
            (impl for impl in game.config.manager if impl not in game.config.service),
            key=lambda impl: game.config.manager[impl][3],
        )
        for dummy in range(2):
            cell = level.business_arolla(builder)
            level.object.factory[cell] = AbstractBusinessFactory.builder_factory(
                game.config, weak, cell
            )
        game.status.service = "An alarm trap! Monsters stir in the dark!"


def i_service(game, item) -> None:
    level = game.world.helper_i()
    magic = game.player.business.service
    if "mapping" in item.service:
        for yy in range(level.executor.default):
            for xx in range(level.executor.common):
                if level.impl_dummy((xx, yy)):
                    level.object.service.add((xx, yy))
        game.status.service = "The dungeon map reveals itself!"
    elif "teleportation" in item.service:
        game.player.data = level.business_arolla(game.world.builder, (game.player.data,))
        game.status.service = "You are teleported!"
    else:
        hits = 0
        for pos in list(level.object.factory):
            monster = level.object.factory[pos]
            if pos in game.visible and not monster.processor:
                monster.utils_data(item.helper + magic)
                hits += 1
                if not monster.i_object:
                    del level.object.factory[pos]
                    game.player.arolla_utils(monster.object)
        game.status.service = f"Fireball! {hits} monsters burn."


def processor_dummy(game, monster) -> None:
    level = game.world.helper_i()
    dmg = arolla_service(game.world.builder, game.player.builder_utils(), monster.executor)
    if dmg == 0:
        game.status.service = f"You miss the {monster.service}."
        return
    monster.utils_data(dmg)
    if not monster.i_object:
        del level.object.factory[monster.data]
        gained = game.player.arolla_utils(monster.object)
        game.status.service = (
            f"You kill the {monster.service}! +{monster.object} xp."
            + (f" Level up: {game.player.arolla}!" if gained else "")
        )
    else:
        game.status.service = f"You hit the {monster.service} for {dmg}."


def i_builder(game) -> None:
    game.business_arolla()
    game.impl_business()
