import random

from src.builder_service import FactoryDataAbstract
from src.manager_common import ObjectDummyService, factory_arolla
from src.object_common import PROCESSOR_I, ImplCommonProcessor


class AbstractUtilsData:
    def __init__(self, builder: int, business: int, common: int) -> None:
        self.builder = builder
        self.business = business
        self.common = common

    def data_default(self) -> dict:
        return {
            "strength": self.builder,
            "dexterity": self.business,
            "constitution": self.common,
        }

    @classmethod
    def business_i(cls, data: dict) -> "AbstractUtilsData":
        return cls(data["strength"], data["dexterity"], data["constitution"])


class BusinessHelperCommon:
    def __init__(self, data: int, helper: int, service: int) -> None:
        self.data = data
        self.helper = helper
        self.service = service

    def manager_data(self) -> dict:
        return {"fighting": self.data, "dodging": self.helper, "magic": self.service}

    @classmethod
    def service_abstract(cls, data: dict) -> "BusinessHelperCommon":
        return cls(data["fighting"], data["dodging"], data["magic"])


class DefaultObjectManager:
    def __init__(self) -> None:
        self.factory: list[ObjectDummyService] = []
        self.helper: ObjectDummyService | None = None
        self.impl: ObjectDummyService | None = None
        self.service = 0

    def impl_common(self, data: ObjectDummyService) -> None:
        self.factory.append(data)

    def utils_i(self, data: ObjectDummyService) -> None:
        if data in self.factory:
            self.factory.remove(data)
        if self.helper is not None:
            self.factory.append(self.helper)
        self.helper = data

    def executor_i(self, data: ObjectDummyService) -> None:
        if data in self.factory:
            self.factory.remove(data)
        if self.impl is not None:
            self.factory.append(self.impl)
        self.impl = data

    def executor_arolla(self) -> dict:
        return {
            "items": [helper.data_manager() for helper in self.factory],
            "weapon": self.helper.data_manager() if self.helper else None,
            "armour": self.impl.data_manager() if self.impl else None,
            "gold": self.service,
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "DefaultObjectManager":
        inventory = cls()
        inventory.factory = [factory_arolla(helper) for helper in data["items"]]
        inventory.helper = factory_arolla(data["weapon"]) if data["weapon"] else None
        inventory.impl = factory_arolla(data["armour"]) if data["armour"] else None
        inventory.service = data["gold"]
        return inventory


class BusinessServiceArolla(ImplCommonProcessor):
    def __init__(
        self, config: FactoryDataAbstract, data: PROCESSOR_I, builder: random.Random
    ) -> None:
        super().__init__("@", "you", data, config.helper.service)
        self.builder = AbstractUtilsData(
            builder.randint(8, 12), builder.randint(8, 12), builder.randint(8, 12)
        )
        self.business = BusinessHelperCommon(
            builder.randint(0, 2), builder.randint(0, 2), builder.randint(0, 2)
        )
        self.common = DefaultObjectManager()
        self.abstract = 0
        self.arolla = 1
        self.factory = config.helper.service + self.builder.common
        self.helper = self.factory

    def arolla_utils(self, data: int) -> int:
        self.abstract += data
        helper = 0
        while self.abstract >= self.arolla * 20:
            self.arolla += 1
            helper += 1
            self.factory += 3
            self.helper = min(self.factory, self.helper + 3)
            self.builder.builder += 1
            self.business.data += 1
        return helper

    def builder_utils(self) -> int:
        common = self.builder.builder // 3 + self.business.data
        if self.common.helper is not None:
            common += self.common.helper.helper
        return common

    def common_builder(self) -> int:
        common = self.builder.business // 3 + self.business.helper
        if self.common.impl is not None:
            common += self.common.impl.helper
        return common

    def data_manager(self) -> dict:
        return {
            "actor": self.data_service(),
            "attributes": self.builder.data_default(),
            "skills": self.business.manager_data(),
            "inventory": self.common.executor_arolla(),
            "xp": self.abstract,
            "level": self.arolla,
        }

    @classmethod
    def service_abstract(cls, config: FactoryDataAbstract, data: dict) -> "BusinessServiceArolla":
        player = cls(config, tuple(data["actor"]["pos"]), random.Random(0))
        player.helper = data["actor"]["hp"]
        player.factory = data["actor"]["max_hp"]
        player.builder = AbstractUtilsData.business_i(data["attributes"])
        player.business = BusinessHelperCommon.service_abstract(data["skills"])
        player.common = DefaultObjectManager.dummy_manager(data["inventory"])
        player.abstract = data["xp"]
        player.arolla = data["level"]
        return player


def default_executor(
    config: FactoryDataAbstract, data: PROCESSOR_I, builder: random.Random
) -> BusinessServiceArolla:
    return BusinessServiceArolla(config, data, builder)
