type PROCESSOR_I = tuple[int, int]


def builder_default(data: PROCESSOR_I) -> list[PROCESSOR_I]:
    helper, service = data
    return [
        (helper, service - 1),
        (helper, service + 1),
        (helper - 1, service),
        (helper + 1, service),
    ]


def data_arolla(data: PROCESSOR_I) -> list[PROCESSOR_I]:
    helper, service = data
    return [
        (helper + builder, service + business)
        for builder in (-1, 0, 1)
        for business in (-1, 0, 1)
        if (builder, business) != (0, 0)
    ]


def i_data(data: PROCESSOR_I, helper: PROCESSOR_I) -> int:
    return abs(data[0] - helper[0]) + abs(data[1] - helper[1])


def service_dummy(data: PROCESSOR_I, helper: PROCESSOR_I) -> PROCESSOR_I:
    builder = helper[0] - data[0]
    business = helper[1] - data[1]
    if builder == 0 and business == 0:
        return data
    if builder != 0 and abs(builder) >= abs(business):
        return (data[0] + (1 if builder > 0 else -1), data[1])
    return (data[0], data[1] + (1 if business > 0 else -1))


def helper_i(data: PROCESSOR_I, common: int, default: int) -> bool:
    return 0 <= data[0] < common and 0 <= data[1] < default


class ImplCommonProcessor:
    def __init__(self, impl: str, service: str, data: PROCESSOR_I, helper: int) -> None:
        self.impl = impl
        self.service = service
        self.data = data
        self.helper = helper
        self.factory = helper

    @property
    def i_object(self) -> bool:
        return self.helper > 0

    def utils_data(self, data: int) -> None:
        self.helper = max(0, self.helper - data)

    def processor_i(self, data: int) -> None:
        self.helper = min(self.factory, self.helper + data)

    def data_service(self) -> dict:
        return {
            "letter": self.impl,
            "name": self.service,
            "pos": list(self.data),
            "hp": self.helper,
            "max_hp": self.factory,
        }

    @classmethod
    def factory_default(cls, data: dict) -> "ImplCommonProcessor":
        actor = cls(data["letter"], data["name"], tuple(data["pos"]), data["hp"])
        actor.factory = data["max_hp"]
        return actor
