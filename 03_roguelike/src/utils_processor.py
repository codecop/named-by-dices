import sys

from src.impl_object import ArollaBusinessFactory

PROCESSOR_ABSTRACT = {
    "quit": "Q",
    "save": "s",
    "help": "?",
    "rest": ".",
    "down": ">",
    "up": "<",
    "get": ",",
    "inventory": "i",
    "look": "i",
}


def executor_i(line: str) -> str:
    word = line.strip().lower()
    if word in PROCESSOR_ABSTRACT:
        return PROCESSOR_ABSTRACT[word]
    return word[:1]


def business_abstract(saver, writer) -> ArollaBusinessFactory:
    def reader() -> str:
        return executor_i(sys.stdin.readline())

    return ArollaBusinessFactory(reader, writer, saver)
