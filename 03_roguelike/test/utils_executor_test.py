import os
import tempfile
import unittest
from pathlib import Path

from src.builder_service import business_utils
from src.impl_object import ArollaBusinessFactory, ManagerIExecutor
from src.utils_executor import business_utils as raw_load
from src.utils_executor import default_service, executor_factory


def utils_common():
    return business_utils(str(Path(__file__).resolve().parent.parent / "game.txt"))


def object_impl(config, seed):
    stream = iter([""] * 10)
    io = ArollaBusinessFactory(stream.__next__, lambda text: None, lambda game: None)
    return ManagerIExecutor(config, seed, io), io


class TestSaveLoad(unittest.TestCase):
    def test_save_and_load_round_trip_restores_state_and_rng(self):
        config = utils_common()
        game, io = object_impl(config, 7)
        game.handle("h")
        game.impl_business()
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "savegame.json")
            executor_factory(game, path)
            payload = raw_load(path)
            self.assertIn("config", payload)
            self.assertIn("rng", payload)
            self.assertIn("game", payload)
            loaded = default_service(path, io)
        self.assertEqual(loaded.executor_arolla(), game.executor_arolla())
        self.assertEqual(
            loaded.world.builder.getstate(), game.world.builder.getstate()
        )

    def test_load_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                raw_load(os.path.join(tmp, "nope.json"))


if __name__ == "__main__":
    unittest.main()
