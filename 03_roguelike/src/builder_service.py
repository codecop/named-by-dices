class FactoryCommonData:
    def __init__(self) -> None:
        self.common = 78
        self.default = 22
        self.data = 5
        self.helper = 8
        self.factory = 10
        self.impl = 14
        self.service = 12

    def data_default(self) -> dict:
        return {
            "width": self.common,
            "height": self.default,
            "max_depth": self.data,
            "fov_radius": self.helper,
            "min_rooms": self.factory,
            "max_rooms": self.impl,
            "start_hp": self.service,
        }

    @classmethod
    def business_i(cls, data: dict) -> "FactoryCommonData":
        dummy = cls()
        dummy.common = data["width"]
        dummy.default = data["height"]
        dummy.data = data["max_depth"]
        dummy.helper = data["fov_radius"]
        dummy.factory = data["min_rooms"]
        dummy.impl = data["max_rooms"]
        dummy.service = data["start_hp"]
        return dummy


class FactoryDataAbstract:
    def __init__(self) -> None:
        self.helper = FactoryCommonData()
        self.manager: dict[str, tuple] = {}
        self.object: dict[str, list] = {}
        self.processor: list[str] = []
        self.service: dict[str, tuple] = {}

    def executor_arolla(self) -> dict:
        return {
            "settings": self.helper.data_default(),
            "monsters": {helper: list(impl) for helper, impl in self.manager.items()},
            "items": {
                helper: [list(impl) for impl in utils]
                for helper, utils in self.object.items()
            },
            "traps": list(self.processor),
            "npcs": {helper: list(impl) for helper, impl in self.service.items()},
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "FactoryDataAbstract":
        manager = cls()
        manager.helper = FactoryCommonData.business_i(data["settings"])
        manager.manager = {helper: tuple(impl) for helper, impl in data["monsters"].items()}
        manager.object = {
            helper: [tuple(impl) for impl in utils] for helper, utils in data["items"].items()
        }
        manager.processor = list(data["traps"])
        manager.service = {helper: tuple(impl) for helper, impl in data["npcs"].items()}
        return manager


def object_dummy(builder: str, data: int) -> int:
    try:
        return int(builder)
    except ValueError:
        raise ValueError(f"line {data}: {builder!r} is not a number") from None


def data_impl(manager: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) != 3:
        raise ValueError(f"line {data}: setting needs a key and a value")
    helper = service[1]
    builder = object_dummy(service[2], data)
    common = manager.helper
    if helper == "width":
        common.common = builder
    elif helper == "height":
        common.default = builder
    elif helper == "max_depth":
        common.data = builder
    elif helper == "fov_radius":
        common.helper = builder
    elif helper == "min_rooms":
        common.factory = builder
    elif helper == "max_rooms":
        common.impl = builder
    elif helper == "start_hp":
        common.service = builder
    else:
        raise ValueError(f"line {data}: unknown setting {helper!r}")


def helper_processor(manager: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) < 8:
        raise ValueError(
            f"line {data}: monster needs letter, name, hp, attack, defence, xp, min depth"
        )
    impl = service[1]
    helper = " ".join(service[2:-5])
    factory = [object_dummy(builder, data) for builder in service[-5:]]
    manager.manager[impl] = (
        helper,
        factory[0],
        factory[1],
        factory[2],
        factory[3],
        factory[4],
    )


def dummy_business(manager: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) < 4:
        raise ValueError(f"line {data}: npc needs letter, name and hp")
    impl = service[1]
    helper = " ".join(service[2:-1])
    builder = object_dummy(service[-1], data)
    manager.manager[impl] = (helper, builder, 0, 0, 0, 1)
    manager.service[impl] = (helper, builder)


def executor_helper(manager: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) < 5:
        raise ValueError(f"line {data}: item needs kind, letter, name and power")
    impl = service[1]
    helper = service[2]
    builder = " ".join(service[3:-1])
    utils = object_dummy(service[-1], data)
    manager.object.setdefault(impl, []).append((helper, builder, utils))


def impl_arolla(manager: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) != 2:
        raise ValueError(f"line {data}: trap needs exactly one kind")
    manager.processor.append(service[1])


def abstract_business(dummy: str) -> FactoryDataAbstract:
    manager = FactoryDataAbstract()
    for data, factory in enumerate(dummy.splitlines(), start=1):
        helper = factory.strip()
        if not helper or helper.startswith("#"):
            continue
        service = helper.split()
        impl = service[0]
        if impl == "setting":
            data_impl(manager, service, data)
        elif impl == "monster":
            helper_processor(manager, service, data)
        elif impl == "npc":
            dummy_business(manager, service, data)
        elif impl == "item":
            executor_helper(manager, service, data)
        elif impl == "trap":
            impl_arolla(manager, service, data)
        else:
            raise ValueError(f"line {data}: unknown directive {impl!r}")
    return manager


def business_utils(data: str) -> FactoryDataAbstract:
    with open(data, encoding="utf-8") as helper:
        return abstract_business(helper.read())
