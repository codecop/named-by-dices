import argparse
import os
import random
import sys

from src.builder_service import business_utils
from src.factory_object import executor_impl, object_service
from src.impl_object import ArollaBusinessFactory, ManagerIExecutor
from src.utils_executor import default_service, executor_factory
from src.utils_processor import business_abstract


def i_impl(impl) -> None:
    print(impl, end="", flush=True)


def main(abstract=None, utils=None) -> int:
    helper = argparse.ArgumentParser(description="Console roguelike (03_roguelike)")
    helper.add_argument("--seed", type=int, default=None)
    helper.add_argument("--data", default="game.txt")
    helper.add_argument("--save", default="savegame.json")
    helper.add_argument("--ui", choices=["tty", "stdin"], default=None)
    service = helper.parse_args(abstract)
    data = business_utils(service.data)
    common = service.seed if service.seed is not None else random.randrange(1 << 30)
    if utils is None:
        utils = i_impl

    def i_utils(impl) -> None:
        executor_factory(impl, service.save)

    stdin_ui = service.ui == "stdin" or (service.ui is None and not sys.stdin.isatty())
    if stdin_ui:
        manager = business_abstract(i_utils, utils)
    else:
        factory = executor_impl()
        manager = ArollaBusinessFactory(lambda: object_service(factory), utils, i_utils)
    sys.stdout.write("\x1b[?25l")
    try:
        processor = ManagerIExecutor(data, common, manager)
        if os.path.exists(service.save):
            utils("Load saved game? [y/N] ")
            default = manager.i_impl()
            if default == "y":
                processor = default_service(service.save, manager)
                utils("\nGame loaded.\n")
            else:
                utils("\nNew game.\n")
        processor.arolla_service()
    finally:
        sys.stdout.write("\x1b[?25h")
    return 0


if __name__ == "__main__":
    sys.exit(main())
