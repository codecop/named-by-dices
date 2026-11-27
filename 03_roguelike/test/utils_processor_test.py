import unittest
from unittest import mock

from src import utils_processor
from src.utils_processor import business_abstract, executor_i


class TestExecutorI(unittest.TestCase):
    def test_single_letters_pass_through(self):
        self.assertEqual(executor_i("h\n"), "h")
        self.assertEqual(executor_i(">"), ">")
        self.assertEqual(executor_i(","), ",")

    def test_words_map_to_commands(self):
        self.assertEqual(executor_i("quit\n"), "Q")
        self.assertEqual(executor_i("DOWN\n"), ">")
        self.assertEqual(executor_i("up\n"), "<")
        self.assertEqual(executor_i("save\n"), "s")
        self.assertEqual(executor_i("help"), "?")
        self.assertEqual(executor_i("rest\n"), ".")
        self.assertEqual(executor_i("get\n"), ",")
        self.assertEqual(executor_i("look\n"), "i")

    def test_empty_line_and_eof_map_to_empty_command(self):
        self.assertEqual(executor_i(""), "")
        self.assertEqual(executor_i("\n"), "")


class TestBusinessAbstract(unittest.TestCase):
    def test_reader_reads_lines_from_stdin_and_maps_them(self):
        helper = mock.Mock()
        helper.readline.side_effect = ["h\n", "quit\n", ""]
        with mock.patch.object(utils_processor, "sys") as sys_mock:
            sys_mock.stdin = helper
            io = business_abstract(lambda impl: None, lambda impl: None)
            self.assertEqual(io.i_impl(), "h")
            self.assertEqual(io.i_impl(), "Q")
            self.assertEqual(io.i_impl(), "")

    def test_writer_and_saver_are_wired_to_the_port(self):
        manager = []
        processor = []
        io = business_abstract(processor.append, manager.append)
        io.i_object("frame")
        io.impl("game")
        self.assertEqual(manager, ["frame"])
        self.assertEqual(processor, ["game"])


if __name__ == "__main__":
    unittest.main()
