import importlib
import sys
import unittest
from unittest import mock

from src import factory_object


class TestObjectService(unittest.TestCase):
    def test_plain_key_is_returned(self):
        self.assertEqual(factory_object.object_service(iter(["h"]).__next__), "h")

    def test_arrow_escape_sequence_maps_to_vi_key(self):
        keys = iter(["\x1b", "[", "A"])
        self.assertEqual(factory_object.object_service(keys.__next__), "k")

    def test_unknown_escape_sequence_returns_empty(self):
        keys = iter(["\x1b", "[", "Z"])
        self.assertEqual(factory_object.object_service(keys.__next__), "")


class TestExecutorImpl(unittest.TestCase):
    def test_piped_stdin_returns_a_plain_reader(self):
        with mock.patch.object(factory_object, "sys") as sys_mock:
            sys_mock.stdin.isatty.return_value = False
            reader = factory_object.executor_impl()
            self.assertTrue(callable(reader))

    def test_windows_tty_uses_msvcrt_getch(self):
        with (
            mock.patch.object(factory_object, "sys") as sys_mock,
            mock.patch.object(factory_object, "os") as os_mock,
        ):
            sys_mock.stdin.isatty.return_value = True
            os_mock.name = "nt"
            reader = factory_object.executor_impl()
            self.assertIs(reader, factory_object.arolla_builder)

    def test_posix_tty_uses_termios_getch(self):
        with (
            mock.patch.object(factory_object, "sys") as sys_mock,
            mock.patch.object(factory_object, "os") as os_mock,
        ):
            sys_mock.stdin.isatty.return_value = True
            os_mock.name = "posix"
            reader = factory_object.executor_impl()
            self.assertIs(reader, factory_object.business_factory)


class TestGetch(unittest.TestCase):
    def test_windows_getch_decodes_the_byte(self):
        with mock.patch.object(factory_object, "msvcrt") as msvcrt_mock:
            msvcrt_mock.getch.return_value = "x".encode()
            self.assertEqual(factory_object.arolla_builder(), "x")

    def test_posix_getch_sets_raw_mode_and_restores(self):
        fake_stdin = mock.Mock()
        fake_stdin.fileno.return_value = 5
        fake_stdin.read.return_value = "h"
        with (
            mock.patch.object(factory_object, "sys") as sys_mock,
            mock.patch.object(factory_object, "termios") as termios_mock,
            mock.patch.object(factory_object, "tty") as tty_mock,
        ):
            sys_mock.stdin = fake_stdin
            termios_mock.tcgetattr.return_value = "old"
            result = factory_object.business_factory()
        self.assertEqual(result, "h")
        tty_mock.setraw.assert_called_once_with(5)
        termios_mock.tcsetattr.assert_called_once_with(
            5, termios_mock.TCSADRAIN, "old"
        )


class TestImportFallbacks(unittest.TestCase):
    def test_module_reloads_when_termios_and_msvcrt_are_missing(self):
        with mock.patch.dict(
            sys.modules, {"termios": None, "tty": None, "msvcrt": None}
        ):
            importlib.reload(factory_object)
            self.assertIsNone(factory_object.termios)
            self.assertIsNone(factory_object.tty)
            self.assertIsNone(factory_object.msvcrt)
        importlib.reload(factory_object)
        self.assertIsNotNone(factory_object.termios)
        self.assertIsNotNone(factory_object.tty)


if __name__ == "__main__":
    unittest.main()
