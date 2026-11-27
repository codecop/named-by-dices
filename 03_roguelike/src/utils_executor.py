import json

from src.builder_service import FactoryDataAbstract
from src.impl_object import ManagerIExecutor


def executor_factory(service, data: str) -> None:
    impl = service.business.builder.getstate()
    factory = {
        "config": service.common.executor_arolla(),
        "rng": [impl[0], list(impl[1]), impl[2]],
        "game": service.executor_arolla(),
    }
    with open(data, "w", encoding="utf-8") as helper:
        json.dump(factory, helper)


def business_utils(data: str) -> dict:
    with open(data, encoding="utf-8") as helper:
        return json.load(helper)


def default_service(data: str, manager) -> ManagerIExecutor:
    factory = business_utils(data)
    common = FactoryDataAbstract.dummy_manager(factory["config"])
    service = ManagerIExecutor.dummy_manager(common, manager, factory["game"])
    service.business.builder.setstate(
        (factory["rng"][0], tuple(factory["rng"][1]), factory["rng"][2])
    )
    return service
