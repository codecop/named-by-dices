import random

from src.builder_service import FactoryDataAbstract
from src.data_common import ManagerBusinessArolla
from src.object_common import PROCESSOR_I, ImplCommonProcessor, data_arolla, i_data, service_dummy


class AbstractBusinessFactory(ImplCommonProcessor):
    def __init__(self, impl: str, service: str, data: PROCESSOR_I, helper: tuple) -> None:
        super().__init__(impl, service, data, helper[0])
        self.manager = helper[1]
        self.executor = helper[2]
        self.object = helper[3]
        self.processor = helper[4]
        self.utils = False

    @classmethod
    def builder_factory(
        cls, common: FactoryDataAbstract, impl: str, data: PROCESSOR_I
    ) -> "AbstractBusinessFactory":
        helper = common.manager[impl]
        return cls(
            impl,
            helper[0],
            data,
            (helper[1], helper[2], helper[3], helper[4], impl in common.service),
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
        helper = cls(
            data["letter"],
            data["name"],
            tuple(data["pos"]),
            (data["hp"], data["attack"], data["defence"], data["xp"], data["friendly"]),
        )
        helper.factory = data["max_hp"]
        helper.utils = data["healed"]
        return helper


def processor_service(
    common: FactoryDataAbstract,
    helper: ManagerBusinessArolla,
    builder: random.Random,
    data: int,
) -> None:
    manager = helper.manager[0]
    processor = builder.randint(6, 10) + data
    dummy = [
        impl
        for impl, arolla in common.manager.items()
        if arolla[5] <= data and impl not in common.service
    ]
    if not dummy:
        return
    service = 0
    utils = 0
    while service < processor and utils < 300:
        utils += 1
        factory = helper.business_arolla(builder)
        if manager.object_default(factory):
            continue
        impl = builder.choice(dummy)
        helper.object.factory[factory] = AbstractBusinessFactory.builder_factory(
            common, impl, factory
        )
        service += 1


def helper_builder(
    common: FactoryDataAbstract, helper: ManagerBusinessArolla, builder: random.Random
) -> None:
    for impl in common.service:
        manager = builder.choice(helper.manager[1:])
        data = manager.processor_factory(builder)
        helper.object.factory[data] = AbstractBusinessFactory.builder_factory(
            common, impl, data
        )


def arolla_executor(
    builder: random.Random,
    helper: ManagerBusinessArolla,
    manager: AbstractBusinessFactory,
    data: PROCESSOR_I,
    executor: bool,
) -> PROCESSOR_I:
    abstract = set(helper.object.factory) | set(helper.object.helper)
    abstract.discard(manager.data)
    if executor:
        if i_data(manager.data, data) == 1:
            return data
        service = service_dummy(manager.data, data)
        if helper.impl_dummy(service) and service not in abstract:
            return service
    common = [
        impl
        for impl in data_arolla(manager.data)
        if helper.impl_dummy(impl) and impl not in abstract and impl != data
    ]
    if common and builder.random() < 0.3:
        return builder.choice(common)
    return manager.data


def dummy_processor(data: dict) -> AbstractBusinessFactory:
    return AbstractBusinessFactory.i_utils(data)
