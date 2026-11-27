import random

from src.builder_service import FactoryDataAbstract
from src.data_common import ManagerBusinessArolla
from src.object_common import PROCESSOR_I, ImplCommonProcessor, data_arolla, i_data, service_dummy


class AbstractBusinessFactory(ImplCommonProcessor):
    def __init__(
        self, impl: str, service: str, data: PROCESSOR_I, stats: tuple
    ) -> None:
        super().__init__(impl, service, data, stats[0])
        self.manager = stats[1]
        self.executor = stats[2]
        self.object = stats[3]
        self.processor = stats[4]
        self.utils = False

    @classmethod
    def builder_factory(
        cls, config: FactoryDataAbstract, impl: str, data: PROCESSOR_I
    ) -> "AbstractBusinessFactory":
        stats = config.manager[impl]
        return cls(
            impl, stats[0], data, (stats[1], stats[2], stats[3], stats[4], impl in config.service)
        )

    def executor_common(self) -> dict:
        return {
            **self.data_service(),
            "attack": self.manager,
            "defence": self.executor,
            "xp": self.object,
            "friendly": self.processor,
            "healed": self.utils,
        }

    @classmethod
    def i_utils(cls, data: dict) -> "AbstractBusinessFactory":
        monster = cls(
            data["letter"],
            data["name"],
            tuple(data["pos"]),
            (data["hp"], data["attack"], data["defence"], data["xp"], data["friendly"]),
        )
        monster.factory = data["max_hp"]
        monster.utils = data["healed"]
        return monster


def processor_service(
    config: FactoryDataAbstract,
    level: ManagerBusinessArolla,
    builder: random.Random,
    data: int,
) -> None:
    helper = level.manager[0]
    common = builder.randint(6, 10) + data
    dummy = [
        impl
        for impl, stats in config.manager.items()
        if stats[5] <= data and impl not in config.service
    ]
    service = 0
    utils = 0
    while service < common and utils < 300:
        utils += 1
        factory = level.business_arolla(builder)
        if helper.object_default(factory):
            continue
        impl = builder.choice(dummy)
        level.object.factory[factory] = AbstractBusinessFactory.builder_factory(
            config, impl, factory
        )
        service += 1


def helper_builder(
    config: FactoryDataAbstract, level: ManagerBusinessArolla, builder: random.Random
) -> None:
    for impl in config.service:
        helper = builder.choice(level.manager[1:])
        data = helper.processor_factory(builder)
        level.object.factory[data] = AbstractBusinessFactory.builder_factory(config, impl, data)


def arolla_executor(
    builder: random.Random,
    level: ManagerBusinessArolla,
    monster: AbstractBusinessFactory,
    helper: PROCESSOR_I,
    can_see: bool,
) -> PROCESSOR_I:
    occupied = set(level.object.factory) | set(level.object.helper)
    occupied.discard(monster.data)
    if can_see and i_data(monster.data, helper) > 1:
        data = service_dummy(monster.data, helper)
        if level.impl_dummy(data) and data not in occupied:
            return data
    common = [
        service
        for service in data_arolla(monster.data)
        if level.impl_dummy(service) and service not in occupied and service != helper
    ]
    if common and builder.random() < 0.3:
        return builder.choice(common)
    return monster.data


def dummy_processor(data: dict) -> AbstractBusinessFactory:
    return AbstractBusinessFactory.i_utils(data)
