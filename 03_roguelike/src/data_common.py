import random

from src.builder_service import FactoryDataAbstract
from src.object_common import PROCESSOR_I, builder_default


class ArollaImplData:
    def __init__(self, abstract: int, arolla: int, common: int, default: int) -> None:
        self.abstract = abstract
        self.arolla = arolla
        self.common = common
        self.default = default

    @property
    def utils_common(self) -> PROCESSOR_I:
        return (self.abstract + self.common // 2, self.arolla + self.default // 2)

    def impl_builder(self, builder: "ArollaImplData") -> bool:
        return not (
            self.abstract + self.common + 1 < builder.abstract
            or builder.abstract + builder.common + 1 < self.abstract
            or self.arolla + self.default + 1 < builder.arolla
            or builder.arolla + builder.default + 1 < self.arolla
        )

    def object_default(self, data: PROCESSOR_I) -> bool:
        return (
            self.abstract <= data[0] < self.abstract + self.common
            and self.arolla <= data[1] < self.arolla + self.default
        )

    def processor_factory(self, builder: random.Random) -> PROCESSOR_I:
        return (
            builder.randint(self.abstract + 1, self.abstract + self.common - 2),
            builder.randint(self.arolla + 1, self.arolla + self.default - 2),
        )

    def service_dummy(self) -> list[PROCESSOR_I]:
        data = []
        for helper in range(self.abstract, self.abstract + self.common):
            data.append((helper, self.arolla))
            data.append((helper, self.arolla + self.default - 1))
        for service in range(self.arolla + 1, self.arolla + self.default - 1):
            data.append((self.abstract, service))
            data.append((self.abstract + self.common - 1, service))
        return data

    def manager_object(self) -> dict:
        return {
            "x": self.abstract,
            "y": self.arolla,
            "width": self.common,
            "height": self.default,
        }

    @classmethod
    def data_arolla(cls, data: dict) -> "ArollaImplData":
        return cls(data["x"], data["y"], data["width"], data["height"])


class ImplProcessorDefault:
    def __init__(self, data: str, helper: bool = False) -> None:
        self.data = data
        self.helper = helper

    def object_factory(self) -> dict:
        return {"kind": self.data, "found": self.helper}

    @classmethod
    def i_utils(cls, data: dict) -> "ImplProcessorDefault":
        return cls(data["kind"], data["found"])


class UtilsCommonExecutor:
    def __init__(self, common: int, default: int) -> None:
        self.common = common
        self.default = default
        self.builder = [["#"] * common for dummy in range(default)]

    def utils_data(self, data: PROCESSOR_I) -> str:
        if not self.i_business(data):
            return "#"
        return self.builder[data[1]][data[0]]

    def helper_executor(self, data: PROCESSOR_I, helper: str) -> None:
        self.builder[data[1]][data[0]] = helper

    def factory_default(self, data: PROCESSOR_I) -> bool:
        return self.utils_data(data) == "#"

    def i_business(self, data: PROCESSOR_I) -> bool:
        return 0 <= data[0] < self.common and 0 <= data[1] < self.default

    def impl_dummy(self, data: PROCESSOR_I) -> bool:
        return self.i_business(data) and not self.factory_default(data)

    def executor_arolla(self) -> dict:
        return {
            "width": self.common,
            "height": self.default,
            "grid": ["".join(helper) for helper in self.builder],
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "UtilsCommonExecutor":
        helper = cls(data["width"], data["height"])
        helper.builder = [list(impl) for impl in data["grid"]]
        return helper


class ServiceObjectCommon:
    def __init__(self) -> None:
        self.factory: dict[PROCESSOR_I, object] = {}
        self.helper: dict[PROCESSOR_I, object] = {}
        self.impl: dict[PROCESSOR_I, ImplProcessorDefault] = {}
        self.service: set[PROCESSOR_I] = set()

    def business_arolla(
        self,
        executor: UtilsCommonExecutor,
        builder: random.Random,
        business: tuple = (),
        common: PROCESSOR_I | None = None,
    ) -> PROCESSOR_I | None:
        for dummy in range(200):
            data = (
                builder.randrange(1, executor.common - 1),
                builder.randrange(1, executor.default - 1),
            )
            if (
                executor.impl_dummy(data)
                and data not in business
                and data not in self.helper
                and data not in self.factory
            ):
                return data
        return common

    def executor_arolla(self) -> dict:
        return {
            "traps": [
                {"pos": list(data), **processor.object_factory()}
                for data, processor in self.impl.items()
            ],
            "explored": [list(data) for data in sorted(self.service)],
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "ServiceObjectCommon":
        helper = cls()
        helper.impl = {
            tuple(processor["pos"]): ImplProcessorDefault.i_utils(processor)
            for processor in data["traps"]
        }
        helper.service = {tuple(impl) for impl in data["explored"]}
        return helper


class ManagerBusinessArolla:
    def __init__(self, common: int, default: int, data: int) -> None:
        self.executor = UtilsCommonExecutor(common, default)
        self.object = ServiceObjectCommon()
        self.data = data
        self.manager: list[ArollaImplData] = []
        self.processor: PROCESSOR_I | None = None
        self.utils: PROCESSOR_I | None = None

    def utils_data(self, data: PROCESSOR_I) -> str:
        return self.executor.utils_data(data)

    def helper_executor(self, data: PROCESSOR_I, helper: str) -> None:
        self.executor.helper_executor(data, helper)

    def factory_default(self, data: PROCESSOR_I) -> bool:
        return self.executor.factory_default(data)

    def i_business(self, data: PROCESSOR_I) -> bool:
        return self.executor.i_business(data)

    def impl_dummy(self, data: PROCESSOR_I) -> bool:
        return self.executor.impl_dummy(data)

    def business_arolla(self, builder: random.Random, business: tuple = ()) -> PROCESSOR_I:
        common = self.manager[0].utils_common if self.manager else (1, 1)
        data = self.object.business_arolla(self.executor, builder, business, common)
        return data if data is not None else common

    def executor_arolla(self) -> dict:
        return {
            "depth": self.data,
            "grid": self.executor.executor_arolla(),
            "entities": self.object.executor_arolla(),
            "rooms": [manager.manager_object() for manager in self.manager],
            "stairs_down": list(self.processor) if self.processor else None,
            "stairs_up": list(self.utils) if self.utils else None,
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "ManagerBusinessArolla":
        helper = cls(data["grid"]["width"], data["grid"]["height"], data["depth"])
        helper.executor = UtilsCommonExecutor.dummy_manager(data["grid"])
        helper.object = ServiceObjectCommon.dummy_manager(data["entities"])
        helper.manager = [ArollaImplData.data_arolla(manager) for manager in data["rooms"]]
        helper.processor = tuple(data["stairs_down"]) if data["stairs_down"] else None
        helper.utils = tuple(data["stairs_up"]) if data["stairs_up"] else None
        return helper


def data_service(
    factory: FactoryDataAbstract, builder: random.Random, data: int
) -> ManagerBusinessArolla:
    helper = ManagerBusinessArolla(factory.helper.common, factory.helper.default, data)
    common = builder.randint(factory.helper.factory, factory.helper.impl)
    i_impl(helper, builder, common)
    impl_business(helper, builder)
    common_helper(helper)
    processor_manager(factory, helper, builder)
    utils_executor(factory, helper, builder)
    return helper


def i_impl(helper: ManagerBusinessArolla, builder: random.Random, common: int) -> None:
    dummy = 0
    while len(helper.manager) < common and dummy < 500:
        dummy += 1
        data = builder.randint(4, 10)
        service = builder.randint(3, 7)
        impl = builder.randint(1, helper.executor.common - data - 2)
        factory = builder.randint(1, helper.executor.default - service - 2)
        manager = ArollaImplData(impl, factory, data, service)
        if any(manager.impl_builder(processor) for processor in helper.manager):
            continue
        helper.manager.append(manager)
        for utils in range(factory, factory + service):
            for abstract in range(impl, impl + data):
                helper.helper_executor((abstract, utils), ".")


def impl_business(helper: ManagerBusinessArolla, builder: random.Random) -> None:
    manager = helper.manager
    for dummy in range(len(manager) - 1):
        i_service(helper, manager[dummy].utils_common, manager[dummy + 1].utils_common, builder)
    if len(manager) > 3:
        dummy = builder.randrange(len(manager) - 2)
        i_service(helper, manager[dummy].utils_common, manager[dummy + 2].utils_common, builder)


def i_service(
    helper: ManagerBusinessArolla,
    data: PROCESSOR_I,
    impl: PROCESSOR_I,
    builder: random.Random,
) -> None:
    if builder.random() < 0.5:
        abstract_processor(helper, data[0], data[1], impl[0], data[1])
        abstract_processor(helper, impl[0], data[1], impl[0], impl[1])
    else:
        abstract_processor(helper, data[0], data[1], data[0], impl[1])
        abstract_processor(helper, data[0], impl[1], impl[0], impl[1])


def abstract_processor(
    helper: ManagerBusinessArolla, abstract: int, arolla: int, common: int, default: int
) -> None:
    if arolla == default:
        for impl in range(min(abstract, common), max(abstract, common) + 1):
            helper.helper_executor((impl, arolla), ".")
    else:
        for service in range(min(arolla, default), max(arolla, default) + 1):
            helper.helper_executor((abstract, service), ".")


def common_helper(helper: ManagerBusinessArolla) -> None:
    for manager in helper.manager:
        for data in manager.service_dummy():
            if helper.utils_data(data) != ".":
                continue
            builder = [
                impl
                for impl in builder_default(data)
                if helper.impl_dummy(impl) and not manager.object_default(impl)
            ]
            if builder:
                helper.helper_executor(data, "+")


def processor_manager(
    factory: FactoryDataAbstract, helper: ManagerBusinessArolla, builder: random.Random
) -> None:
    manager = helper.manager[0]
    helper.utils = manager.processor_factory(builder)
    helper.helper_executor(helper.utils, "<")
    if helper.data < factory.helper.data:
        service = builder.choice(helper.manager[1:])
        data = service.processor_factory(builder)
        dummy = 0
        while data == helper.utils and dummy < 20:
            data = service.processor_factory(builder)
            dummy += 1
        helper.processor = data
        helper.helper_executor(data, ">")


def utils_executor(
    factory: FactoryDataAbstract, helper: ManagerBusinessArolla, builder: random.Random
) -> None:
    if not factory.processor:
        return
    common = builder.randint(3, 6)
    manager = helper.manager[0]
    data = 0
    service = 0
    while data < common and service < 200:
        service += 1
        impl = helper.business_arolla(builder, (helper.processor, helper.utils))
        if manager.object_default(impl) or impl in helper.object.impl:
            continue
        processor = builder.choice(factory.processor)
        helper.object.impl[impl] = ImplProcessorDefault(processor)
        data += 1
