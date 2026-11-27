import random

from src.builder_dummy import helper_arolla, impl_common
from src.builder_service import FactoryDataAbstract
from src.business_helper import utils_default
from src.data_common import ManagerBusinessArolla, data_service
from src.executor_service import arolla_service
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
        abstract = cls()
        abstract.data = data["over"]
        abstract.helper = data["won"]
        abstract.service = data["message"]
        return abstract


class DefaultFactoryData:
    def __init__(self, common: FactoryDataAbstract, data: int) -> None:
        self.builder = random.Random(data)
        self.factory: dict[int, ManagerBusinessArolla] = {}
        self.data = 1
        self.i_impl(common, 1)

    def helper_i(self) -> ManagerBusinessArolla:
        return self.factory[self.data]

    def i_impl(self, common: FactoryDataAbstract, data: int) -> None:
        self.data = data
        if data not in self.factory:
            helper = data_service(common, self.builder, data)
            default_service(common, helper, self.builder, data)
            self.factory[data] = helper

    def manager_object(self, helper: ManagerBusinessArolla) -> dict:
        return {
            **helper.executor_arolla(),
            "monsters": [manager.executor_common() for manager in helper.object.factory.values()],
            "items": [
                {"pos": list(data), "item": impl.data_manager()}
                for data, impl in helper.object.helper.items()
            ],
        }

    def executor_arolla(self) -> dict:
        return {
            "depth": self.data,
            "levels": {
                str(data): self.manager_object(helper)
                for data, helper in self.factory.items()
            },
        }

    @classmethod
    def dummy_manager(cls, common: FactoryDataAbstract, dummy: dict) -> "DefaultFactoryData":
        business = cls(common, 0)
        business.factory = {}
        for data, utils in dummy["levels"].items():
            helper = ManagerBusinessArolla.dummy_manager(utils)
            helper.object.factory = {
                tuple(impl["pos"]): dummy_processor(impl) for impl in utils["monsters"]
            }
            helper.object.helper = {
                tuple(impl["pos"]): factory_arolla(impl["item"]) for impl in utils["items"]
            }
            business.factory[int(data)] = helper
        business.data = dummy["depth"]
        return business


class ManagerIExecutor:
    def __init__(self, common: FactoryDataAbstract, data: int, utils) -> None:
        self.common = common
        self.business = DefaultFactoryData(common, data)
        self.utils = utils
        self.executor = set()
        self.abstract = ObjectUtilsI()
        self.factory = default_executor(
            common, self.business.helper_i().manager[0].utils_common, self.business.builder
        )

    def arolla_service(self) -> None:
        while not self.abstract.data:
            self.utils.i_object(utils_default(self))
            self.helper_executor(self.utils.i_impl())
        self.utils.i_object(utils_default(self))

    def helper_executor(self, data: str) -> None:
        processor = True
        if data in UTILS_DEFAULT:
            self.i_impl(UTILS_DEFAULT[data])
        elif data == ".":
            pass
        elif data in (">", "<", ",", "q", "r", "z", "w", "W"):
            self.i_business(data)
        elif data == "i":
            self.abstract.service = self.common_manager()
            processor = False
        elif data == "s":
            self.utils.impl(self)
            self.abstract.service = "Game saved."
            processor = False
        elif data in ("Q", ""):
            self.abstract.data = True
            processor = False
        elif data == "?":
            self.abstract.service = DUMMY_UTILS
            processor = False
        else:
            self.abstract.service = f"Unknown key {data!r}"
            processor = False
        if processor:
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
        helper = self.business.helper_i()
        impl = (self.factory.data[0] + data[0], self.factory.data[1] + data[1])
        if not helper.impl_dummy(impl):
            self.abstract.service = "A wall."
            return
        manager = helper.object.factory.get(impl)
        if manager is not None:
            if manager.processor:
                self.i_utils(manager)
            else:
                processor_dummy(self, manager)
            return
        self.factory.data = impl
        service = helper.object.impl.get(impl)
        if service is not None and not service.helper:
            service_arolla(self, service)

    def i_utils(self, manager) -> None:
        if manager.utils:
            self.abstract.service = "The hermit: 'The Golden Die lies below the dragon.'"
        else:
            manager.utils = True
            self.factory.helper = self.factory.factory
            self.abstract.service = "The hermit heals you completely!"

    def i_object(self) -> None:
        helper = self.business.helper_i()
        data = self.factory.data
        impl = helper.object.helper.get(data)
        if impl is None:
            self.abstract.service = "Nothing here."
            return
        del helper.object.helper[data]
        if impl.data == "gold":
            self.factory.common.service += impl.helper
            self.abstract.service = f"You pick up {impl.helper} gold."
        elif impl.data == "artefact":
            self.factory.common.impl_common(impl)
            self.abstract.service = impl_common("amulet")
        else:
            self.factory.common.impl_common(impl)
            self.abstract.service = f"You pick up {impl.manager_abstract()}."

    def common_helper(self, data: str):
        factory = [impl for impl in self.factory.common.factory if impl.data == data]
        if not factory:
            self.abstract.service = f"No {data} in your inventory."
            return None
        if len(factory) == 1:
            return factory[0]
        helper = ", ".join(
            f"{chr(97 + service)}: {impl.manager_abstract()}"
            for service, impl in enumerate(factory)
        )
        self.abstract.service = f"Use which? {helper}"
        self.utils.i_object(utils_default(self))
        default = self.utils.i_impl()
        service = ord(default) - 97 if default else -1
        if 0 <= service < len(factory):
            return factory[service]
        self.abstract.service = "Never mind."
        return None

    def utils_data(self) -> None:
        impl = self.common_helper("potion")
        if impl is None:
            return
        self.factory.common.factory.remove(impl)
        if impl.helper > 0:
            self.factory.processor_i(impl.helper)
            self.abstract.service = f"You quaff {impl.manager_abstract()}. +{impl.helper} hp."
        else:
            self.factory.utils_data(-impl.helper)
            self.abstract.service = f"You quaff {impl.manager_abstract()}. It burns!"

    def processor_i(self) -> None:
        impl = self.common_helper("scroll")
        if impl is None:
            return
        self.factory.common.factory.remove(impl)
        i_service(self, impl)

    def data_service(self) -> None:
        impl = self.common_helper("wand")
        if impl is None:
            return
        if impl.factory <= 0:
            self.abstract.service = "The wand is drained."
            return
        self.abstract.service = "Zap which way? (hjkl)"
        self.utils.i_object(utils_default(self))
        default = self.utils.i_impl()
        helper = UTILS_DEFAULT.get(default)
        if helper is None:
            self.abstract.service = "Never mind."
            return
        business = self.business.helper_i()
        data = self.factory.data
        factory = 4 + self.factory.business.service
        for dummy in range(20):
            data = (data[0] + helper[0], data[1] + helper[1])
            if not business.impl_dummy(data):
                self.abstract.service = "The bolt fizzles into the wall."
                break
            manager = business.object.factory.get(data)
            if manager is not None and not manager.processor:
                service = arolla_service(self.business.builder, factory, manager.executor)
                manager.utils_data(service)
                if not manager.i_object:
                    del business.object.factory[data]
                    self.factory.arolla_utils(manager.object)
                self.abstract.service = f"Your bolt hits the {manager.service} for {service}."
                break
        impl.factory -= 1
        if impl.factory <= 0:
            self.factory.common.factory.remove(impl)
            self.abstract.service += " The wand crumbles to dust."

    def factory_default(self) -> None:
        impl = self.common_helper("weapon")
        if impl is not None:
            self.factory.common.utils_i(impl)
            self.abstract.service = f"You wield {impl.manager_abstract()}."

    def arolla_utils(self) -> None:
        impl = self.common_helper("armour")
        if impl is not None:
            self.factory.common.executor_i(impl)
            self.abstract.service = f"You wear {impl.manager_abstract()}."

    def common_manager(self) -> str:
        dummy = [impl.manager_abstract() for impl in self.factory.common.factory]
        if self.factory.common.helper is not None:
            dummy.append("wielding " + self.factory.common.helper.manager_abstract())
        if self.factory.common.impl is not None:
            dummy.append("wearing " + self.factory.common.impl.manager_abstract())
        if not dummy:
            return "Inventory is empty."
        return "Inventory: " + ", ".join(dummy)

    def common_builder(self) -> None:
        helper = self.business.helper_i()
        if self.factory.data != helper.processor:
            self.abstract.service = "No stairs down here."
            return
        self.business.i_impl(self.common, self.business.data + 1)
        self.factory.data = self.business.helper_i().manager[0].utils_common
        self.abstract.service = helper_arolla(self.business.data)

    def executor_i(self) -> None:
        helper = self.business.helper_i()
        if self.factory.data != helper.utils:
            self.abstract.service = "No stairs up here."
            return
        if self.business.data == 1:
            if any(impl.data == "artefact" for impl in self.factory.common.factory):
                self.abstract.helper = True
                self.abstract.data = True
                self.abstract.service = impl_common("win")
            else:
                self.abstract.service = "The exit is sealed. You need the artefact!"
            return
        self.business.i_impl(self.common, self.business.data - 1)
        self.factory.data = self.business.helper_i().manager[0].utils_common
        self.abstract.service = f"You climb up to depth {self.business.data}."

    def business_arolla(self) -> None:
        helper = self.business.helper_i()
        for data in list(helper.object.factory):
            manager = helper.object.factory[data]
            if manager.processor or not manager.i_object:
                continue
            impl = data in self.executor
            service = arolla_executor(
                self.business.builder, helper, manager, self.factory.data, impl
            )
            if service == self.factory.data:
                self.i_data(manager)
            elif service != data:
                del helper.object.factory[data]
                helper.object.factory[service] = manager
                manager.data = service

    def i_data(self, manager) -> None:
        factory = arolla_service(
            self.business.builder, manager.manager, self.factory.common_builder()
        )
        if factory == 0:
            self.abstract.service = f"The {manager.service} misses you."
            return
        self.factory.utils_data(factory)
        self.abstract.service = f"The {manager.service} hits you for {factory}."
        if not self.factory.i_object:
            self.abstract.data = True
            self.abstract.service = impl_common("death")

    def impl_business(self) -> None:
        helper = self.business.helper_i()
        self.executor = arolla_utils(
            helper.executor, self.factory.data, self.common.helper.helper
        )
        helper.object.service |= self.executor

    def executor_arolla(self) -> dict:
        return {
            "world": self.business.executor_arolla(),
            "player": self.factory.data_manager(),
            "visible": [list(data) for data in sorted(self.executor)],
            "status": self.abstract.executor_arolla(),
        }

    @classmethod
    def dummy_manager(cls, common: FactoryDataAbstract, utils, data: dict) -> "ManagerIExecutor":
        service = cls(common, 0, utils)
        service.business = DefaultFactoryData.dummy_manager(common, data["world"])
        service.factory = BusinessServiceArolla.service_abstract(common, data["player"])
        service.executor = {tuple(impl) for impl in data["visible"]}
        service.abstract = ObjectUtilsI.dummy_manager(data["status"])
        return service


def default_service(
    common: FactoryDataAbstract, helper: ManagerBusinessArolla, builder: random.Random, data: int
) -> None:
    processor_service(common, helper, builder, data)
    helper_builder(common, helper, builder)
    manager = builder.randint(3, 6)
    if common.object:
        for dummy in range(manager):
            factory = helper.business_arolla(builder)
            helper.object.helper[factory] = executor_factory(common, builder, data)
    if data == common.helper.data:
        service = helper.manager[-1]
        if "artefact" in common.object:
            impl = service.processor_factory(builder)
            helper.object.helper[impl] = object_arolla(common)
        dummy = [impl for impl in common.manager if impl not in common.service]
        if dummy:
            abstract = max(dummy, key=lambda impl: common.manager[impl][5])
            executor = service.processor_factory(builder)
            helper.object.factory[executor] = AbstractBusinessFactory.builder_factory(
                common, abstract, executor
            )


def service_arolla(service, processor) -> None:
    processor.helper = True
    helper = service.business.helper_i()
    builder = service.business.builder
    if processor.data == "dart":
        factory = builder.randint(1, 4)
        service.factory.utils_data(factory)
        service.abstract.service = f"A dart trap hits you for {factory}."
    elif processor.data == "teleport":
        service.factory.data = helper.business_arolla(builder, (service.factory.data,))
        service.abstract.service = "A teleport trap whisks you away!"
    else:
        arolla = min(
            (impl for impl in service.common.manager if impl not in service.common.service),
            key=lambda impl: service.common.manager[impl][3],
        )
        for dummy in range(2):
            data = helper.business_arolla(builder)
            helper.object.factory[data] = AbstractBusinessFactory.builder_factory(
                service.common, arolla, data
            )
        service.abstract.service = "An alarm trap! Monsters stir in the dark!"


def i_service(service, impl) -> None:
    helper = service.business.helper_i()
    factory = service.factory.business.service
    if "mapping" in impl.service:
        for builder in range(helper.executor.default):
            for business in range(helper.executor.common):
                if helper.impl_dummy((business, builder)):
                    helper.object.service.add((business, builder))
        service.abstract.service = "The dungeon map reveals itself!"
    elif "teleportation" in impl.service:
        service.factory.data = helper.business_arolla(
            service.business.builder, (service.factory.data,)
        )
        service.abstract.service = "You are teleported!"
    else:
        manager = 0
        for data in list(helper.object.factory):
            processor = helper.object.factory[data]
            if data in service.executor and not processor.processor:
                processor.utils_data(impl.helper + factory)
                manager += 1
                if not processor.i_object:
                    del helper.object.factory[data]
                    service.factory.arolla_utils(processor.object)
        service.abstract.service = f"Fireball! {manager} monsters burn."


def processor_dummy(service, manager) -> None:
    helper = service.business.helper_i()
    factory = arolla_service(
        service.business.builder, service.factory.builder_utils(), manager.executor
    )
    if factory == 0:
        service.abstract.service = f"You miss the {manager.service}."
        return
    manager.utils_data(factory)
    if not manager.i_object:
        del helper.object.factory[manager.data]
        dummy = service.factory.arolla_utils(manager.object)
        service.abstract.service = (
            f"You kill the {manager.service}! +{manager.object} xp."
            + (f" Level up: {service.factory.arolla}!" if dummy else "")
        )
    else:
        service.abstract.service = f"You hit the {manager.service} for {factory}."


def i_builder(service) -> None:
    service.business_arolla()
    service.impl_business()
