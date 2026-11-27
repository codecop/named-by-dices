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
        helper = cls()
        helper.factory = [factory_arolla(impl) for impl in data["items"]]
        helper.helper = factory_arolla(data["weapon"]) if data["weapon"] else None
        helper.impl = factory_arolla(data["armour"]) if data["armour"] else None
        helper.service = data["gold"]
        return helper


class BusinessServiceArolla(ImplCommonProcessor):
    def __init__(
        self, common: FactoryDataAbstract, data: PROCESSOR_I, builder: random.Random
    ) -> None:
        super().__init__("@", "you", data, common.helper.service)
        self.builder = AbstractUtilsData(
            builder.randint(8, 12), builder.randint(8, 12), builder.randint(8, 12)
        )
        self.business = BusinessHelperCommon(
            builder.randint(0, 2), builder.randint(0, 2), builder.randint(0, 2)
        )
        self.common = DefaultObjectManager()
        self.abstract = 0
        self.arolla = 1
        self.factory = common.helper.service + self.builder.common
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
    def service_abstract(cls, common: FactoryDataAbstract, data: dict) -> "BusinessServiceArolla":
        helper = cls(common, tuple(data["actor"]["pos"]), random.Random(0))
        helper.helper = data["actor"]["hp"]
        helper.factory = data["actor"]["max_hp"]
        helper.builder = AbstractUtilsData.business_i(data["attributes"])
        helper.business = BusinessHelperCommon.service_abstract(data["skills"])
        helper.common = DefaultObjectManager.dummy_manager(data["inventory"])
        helper.abstract = data["xp"]
        helper.arolla = data["level"]
        return helper


def default_executor(
    common: FactoryDataAbstract, data: PROCESSOR_I, builder: random.Random
) -> BusinessServiceArolla:
    return BusinessServiceArolla(common, data, builder)
