import argparse
import os
import random
import sys

from src.builder_service import business_utils
from src.factory_object import executor_impl, object_service
from src.impl_object import ArollaBusinessFactory, ManagerIExecutor
from src.utils_executor import default_service, executor_factory


def i_impl(text) -> None:
    print(text, end="", flush=True)


def main(abstract=None, builder=None) -> int:
    helper = argparse.ArgumentParser(description="Console roguelike (03_roguelike)")
    helper.add_argument("--seed", type=int, default=None)
    helper.add_argument("--data", default="game.txt")
    helper.add_argument("--save", default="savegame.json")
    service = helper.parse_args(abstract)
    data = business_utils(service.data)
    common = service.seed if service.seed is not None else random.randrange(1 << 30)
    factory = executor_impl()
    if builder is None:
        builder = i_impl
    io = ArollaBusinessFactory(
        lambda: object_service(factory),
        builder,
        lambda game: executor_factory(game, service.save),
    )
    sys.stdout.write("\x1b[?25l")
    try:
        game = ManagerIExecutor(data, common, io)
        if os.path.exists(service.save):
            builder("Load saved game? [y/N] ")
            key = object_service(factory)
            if key == "y":
                game = default_service(service.save, io)
                builder("\nGame loaded.\n")
            else:
                builder("\nNew game.\n")
        game.play()
    finally:
        sys.stdout.write("\x1b[?25h")
    return 0


if __name__ == "__main__":
    sys.exit(main())
