import random

from src.builder_service import FactoryDataAbstract


class ObjectDummyService:
    def __init__(
        self, impl: str, service: str, data: str, helper: int, factory: int = 0
    ) -> None:
        self.impl = impl
        self.service = service
        self.data = data
        self.helper = helper
        self.factory = factory

    def manager_abstract(self) -> str:
        return self.service

    def data_manager(self) -> dict:
        return {
            "letter": self.impl,
            "name": self.service,
            "kind": self.data,
            "power": self.helper,
            "charges": self.factory,
        }

    @classmethod
    def service_abstract(cls, data: dict) -> "ObjectDummyService":
        return cls(
            data["letter"], data["name"], data["kind"], data["power"], data["charges"]
        )


def executor_factory(
    common: FactoryDataAbstract, builder: random.Random, data: int
) -> ObjectDummyService:
    dummy = []
    for service in common.object:
        if service == "artefact":
            continue
        dummy.extend([service] * (2 if service in ("potion", "gold") else 1))
    service = builder.choice(dummy)
    helper, impl, utils = builder.choice(common.object[service])
    if service in ("weapon", "armour"):
        utils += data // 2
    elif service == "gold":
        utils = builder.randint(10, 30) * data
    factory = utils if service == "wand" else 0
    return ObjectDummyService(helper, impl, service, utils, factory)


def factory_arolla(data: dict) -> ObjectDummyService:
    return ObjectDummyService.service_abstract(data)


def object_arolla(common: FactoryDataAbstract) -> ObjectDummyService:
    helper, impl, utils = common.object["artefact"][0]
    return ObjectDummyService(helper, impl, "artefact", utils)
