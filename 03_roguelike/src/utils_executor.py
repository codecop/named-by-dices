import json

from src.builder_service import FactoryDataAbstract
from src.impl_object import ManagerIExecutor


def executor_factory(game, data: str) -> None:
    state = game.world.builder.getstate()
    payload = {
        "config": game.config.executor_arolla(),
        "rng": [state[0], list(state[1]), state[2]],
        "game": game.executor_arolla(),
    }
    with open(data, "w", encoding="utf-8") as helper:
        json.dump(payload, helper)


def business_utils(data: str) -> dict:
    with open(data, encoding="utf-8") as helper:
        return json.load(helper)


def default_service(data: str, io) -> ManagerIExecutor:
    payload = business_utils(data)
    config = FactoryDataAbstract.dummy_manager(payload["config"])
    game = ManagerIExecutor.dummy_manager(config, io, payload["game"])
    game.world.builder.setstate(
        (payload["rng"][0], tuple(payload["rng"][1]), payload["rng"][2])
    )
    return game
