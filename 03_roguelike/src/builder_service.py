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
        settings = cls()
        settings.common = data["width"]
        settings.default = data["height"]
        settings.data = data["max_depth"]
        settings.helper = data["fov_radius"]
        settings.factory = data["min_rooms"]
        settings.impl = data["max_rooms"]
        settings.service = data["start_hp"]
        return settings


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
            "monsters": {key: list(value) for key, value in self.manager.items()},
            "items": {
                key: [list(entry) for entry in value] for key, value in self.object.items()
            },
            "traps": list(self.processor),
            "npcs": {key: list(value) for key, value in self.service.items()},
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "FactoryDataAbstract":
        game = cls()
        game.helper = FactoryCommonData.business_i(data["settings"])
        game.manager = {key: tuple(value) for key, value in data["monsters"].items()}
        game.object = {
            key: [tuple(entry) for entry in value] for key, value in data["items"].items()
        }
        game.processor = list(data["traps"])
        game.service = {key: tuple(value) for key, value in data["npcs"].items()}
        return game


def object_dummy(builder: str, data: int) -> int:
    try:
        return int(builder)
    except ValueError:
        raise ValueError(f"line {data}: {builder!r} is not a number") from None


def data_impl(game: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) != 3:
        raise ValueError(f"line {data}: setting needs a key and a value")
    helper = service[1]
    builder = object_dummy(service[2], data)
    settings = game.helper
    if helper == "width":
        settings.common = builder
    elif helper == "height":
        settings.default = builder
    elif helper == "max_depth":
        settings.data = builder
    elif helper == "fov_radius":
        settings.helper = builder
    elif helper == "min_rooms":
        settings.factory = builder
    elif helper == "max_rooms":
        settings.impl = builder
    elif helper == "start_hp":
        settings.service = builder
    else:
        raise ValueError(f"line {data}: unknown setting {helper!r}")


def helper_processor(game: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) < 8:
        raise ValueError(
            f"line {data}: monster needs letter, name, hp, attack, defence, xp, min depth"
        )
    impl = service[1]
    helper = " ".join(service[2:-5])
    factory = [object_dummy(builder, data) for builder in service[-5:]]
    game.manager[impl] = (helper, factory[0], factory[1], factory[2], factory[3], factory[4])


def dummy_business(game: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) < 4:
        raise ValueError(f"line {data}: npc needs letter, name and hp")
    impl = service[1]
    helper = " ".join(service[2:-1])
    builder = object_dummy(service[-1], data)
    game.manager[impl] = (helper, builder, 0, 0, 0, 1)
    game.service[impl] = (helper, builder)


def executor_helper(game: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) < 5:
        raise ValueError(f"line {data}: item needs kind, letter, name and power")
    impl = service[1]
    helper = service[2]
    builder = " ".join(service[3:-1])
    utils = object_dummy(service[-1], data)
    game.object.setdefault(impl, []).append((helper, builder, utils))


def impl_arolla(game: FactoryDataAbstract, service: list, data: int) -> None:
    if len(service) != 2:
        raise ValueError(f"line {data}: trap needs exactly one kind")
    game.processor.append(service[1])


def abstract_business(text: str) -> FactoryDataAbstract:
    game = FactoryDataAbstract()
    for data, raw in enumerate(text.splitlines(), start=1):
        helper = raw.strip()
        if not helper or helper.startswith("#"):
            continue
        service = helper.split()
        impl = service[0]
        if impl == "setting":
            data_impl(game, service, data)
        elif impl == "monster":
            helper_processor(game, service, data)
        elif impl == "npc":
            dummy_business(game, service, data)
        elif impl == "item":
            executor_helper(game, service, data)
        elif impl == "trap":
            impl_arolla(game, service, data)
        else:
            raise ValueError(f"line {data}: unknown directive {impl!r}")
    return game


def business_utils(data: str) -> FactoryDataAbstract:
    with open(data, encoding="utf-8") as helper:
        return abstract_business(helper.read())
