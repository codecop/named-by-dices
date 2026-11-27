import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src import factory_object, main

GAME_TXT = Path(__file__).resolve().parent.parent / "game.txt"


def object_impl(factory):
    fake_stdin = mock.Mock()
    fake_stdin.isatty.return_value = False
    fake_stdin.read.side_effect = list(factory) + [""] * 50
    return fake_stdin


class TestMain(unittest.TestCase):
    def executor_dummy(self, factory, data):
        written = []
        fake_stdin = object_impl(factory)
        with (
            mock.patch.object(factory_object, "sys") as factory_sys,
            mock.patch.object(main, "sys") as main_sys,
        ):
            factory_sys.stdin = fake_stdin
            main_sys.stdout = mock.Mock()
            rc = main.main(
                ["--seed", "7", "--data", str(GAME_TXT), "--save", data],
                utils=written.append,
            )
        return rc, written

    def test_main_runs_a_piped_game_and_quits_on_eof(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, written = self.executor_dummy(["h", "l", "Q"], os.path.join(tmp, "save.json"))
        self.assertEqual(rc, 0)
        self.assertTrue(written)
        self.assertTrue(written[0].startswith("\x1b[2J\x1b[H"))
        self.assertIn("HP", written[0])

    def test_main_saves_and_offers_load_on_next_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            save = os.path.join(tmp, "save.json")
            rc, _ = self.executor_dummy(["s", "Q"], save)
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(save))
            rc, written = self.executor_dummy(["y", "Q"], save)
            self.assertEqual(rc, 0)
            self.assertTrue(any("Game loaded." in text for text in written))

    def test_main_new_game_when_save_declined(self):
        with tempfile.TemporaryDirectory() as tmp:
            save = os.path.join(tmp, "save.json")
            self.executor_dummy(["s", "Q"], save)
            rc, written = self.executor_dummy(["n", "Q"], save)
            self.assertEqual(rc, 0)
            self.assertTrue(any("New game." in text for text in written))

    def test_i_impl_prints_without_newline(self):
        with mock.patch("builtins.print") as print_mock:
            main.i_impl("hello")
        print_mock.assert_called_once_with("hello", end="", flush=True)

    def test_main_without_seed_and_writer_uses_defaults(self):
        fake_stdin = object_impl(["Q"])
        with (
            tempfile.TemporaryDirectory() as tmp,
            mock.patch.object(factory_object, "sys") as factory_sys,
            mock.patch.object(main, "sys") as main_sys,
            mock.patch("builtins.print") as print_mock,
        ):
            factory_sys.stdin = fake_stdin
            main_sys.stdout = mock.Mock()
            rc = main.main(
                ["--data", str(GAME_TXT), "--save", os.path.join(tmp, "s.json")]
            )
        self.assertEqual(rc, 0)
        print_mock.assert_called()


if __name__ == "__main__":
    unittest.main()
