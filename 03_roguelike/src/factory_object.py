import os
import sys

try:
    import msvcrt
except ImportError:
    msvcrt = None

try:
    import termios
    import tty
except ImportError:
    termios = None
    tty = None


def arolla_builder() -> str:
    return msvcrt.getch().decode("utf-8", "replace")


def business_factory() -> str:
    data = sys.stdin.fileno()
    helper = termios.tcgetattr(data)
    try:
        tty.setraw(data)
        service = sys.stdin.read(1)
    finally:
        termios.tcsetattr(data, termios.TCSADRAIN, helper)
    return service


def executor_impl():
    if not sys.stdin.isatty():
        return lambda: sys.stdin.read(1)
    if os.name == "nt":
        return arolla_builder
    return business_factory


def object_service(getch) -> str:
    data = getch()
    if data == "\x1b":
        helper = getch()
        service = getch()
        common = {"[A": "k", "[B": "j", "[C": "l", "[D": "h"}
        return common.get(helper + service, "")
    return data
