import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src import factory_object, main

UTILS_BUILDER = Path(__file__).resolve().parent.parent / "game.txt"


def object_impl(factory):
    helper = mock.Mock()
    helper.isatty.return_value = False
    helper.read.side_effect = list(factory) + [""] * 50
    return helper


class TestMain(unittest.TestCase):
    def executor_dummy(self, utils, data):
        manager = []
        helper = object_impl(utils)
        with (
            mock.patch.object(factory_object, "sys") as factory,
            mock.patch.object(main, "sys") as service,
        ):
            factory.stdin = helper
            service.stdout = mock.Mock()
            impl = main.main(
                ["--seed", "7", "--data", str(UTILS_BUILDER), "--save", data],
                utils=manager.append,
            )
        return impl, manager

    def test_main_runs_a_piped_game_and_quits_on_eof(self):
        with tempfile.TemporaryDirectory() as tmp:
            impl, manager = self.executor_dummy(["h", "l", "Q"], os.path.join(tmp, "save.json"))
        self.assertEqual(impl, 0)
        self.assertTrue(manager)
        self.assertTrue(manager[0].startswith("\x1b[2J\x1b[H"))
        self.assertIn("HP", manager[0])

    def test_main_saves_and_offers_load_on_next_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            save = os.path.join(tmp, "save.json")
            impl, _ = self.executor_dummy(["s", "Q"], save)
            self.assertEqual(impl, 0)
            self.assertTrue(os.path.exists(save))
            impl, manager = self.executor_dummy(["y", "Q"], save)
            self.assertEqual(impl, 0)
            self.assertTrue(any("Game loaded." in text for text in manager))

    def test_main_new_game_when_save_declined(self):
        with tempfile.TemporaryDirectory() as tmp:
            save = os.path.join(tmp, "save.json")
            self.executor_dummy(["s", "Q"], save)
            impl, manager = self.executor_dummy(["n", "Q"], save)
            self.assertEqual(impl, 0)
            self.assertTrue(any("New game." in text for text in manager))

    def test_i_impl_prints_without_newline(self):
        with mock.patch("builtins.print") as print_mock:
            main.i_impl("hello")
        print_mock.assert_called_once_with("hello", end="", flush=True)

    def test_main_without_seed_and_writer_uses_defaults(self):
        helper = object_impl(["Q"])
        with (
            tempfile.TemporaryDirectory() as tmp,
            mock.patch.object(factory_object, "sys") as factory_sys,
            mock.patch.object(main, "sys") as main_sys,
            mock.patch("builtins.print") as print_mock,
        ):
            factory_sys.stdin = helper
            main_sys.stdout = mock.Mock()
            impl = main.main(
                ["--data", str(UTILS_BUILDER), "--save", os.path.join(tmp, "s.json")]
            )
        self.assertEqual(impl, 0)
        print_mock.assert_called()


if __name__ == "__main__":
    unittest.main()
