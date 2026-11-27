"""Position helpers and the actor base class."""

PROCESSOR_I = tuple[int, int]


def builder_default(pos: PROCESSOR_I) -> list[PROCESSOR_I]:
    """Return the four orthogonal neighbours of pos."""
    x, y = pos
    return [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]


def data_arolla(pos: PROCESSOR_I) -> list[PROCESSOR_I]:
    """Return the eight surrounding neighbours of pos."""
    x, y = pos
    return [
        (x + dx, y + dy)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        if (dx, dy) != (0, 0)
    ]


def i_data(a: PROCESSOR_I, b: PROCESSOR_I) -> int:
    """Return the Manhattan distance between a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def service_dummy(src: PROCESSOR_I, dst: PROCESSOR_I) -> PROCESSOR_I:
    """Return one eight-directional step from src towards dst."""
    dx = dst[0] - src[0]
    dy = dst[1] - src[1]
    if dx == 0 and dy == 0:
        return src
    if dx != 0 and abs(dx) >= abs(dy):
        return (src[0] + (1 if dx > 0 else -1), src[1])
    return (src[0], src[1] + (1 if dy > 0 else -1))


def helper_i(pos: PROCESSOR_I, width: int, height: int) -> bool:
    """Return whether pos lies inside a grid of the given size."""
    return 0 <= pos[0] < width and 0 <= pos[1] < height


class ImplCommonProcessor:
    """Base class for actors: the player, monsters and helpers."""

    def __init__(self, letter: str, name: str, pos: PROCESSOR_I, hp: int) -> None:
        self.letter = letter
        self.name = name
        self.pos = pos
        self.hp = hp
        self.max_hp = hp

    @property
    def i_object(self) -> bool:
        """Return whether the actor is still alive."""
        return self.hp > 0

    def utils_data(self, amount: int) -> None:
        """Reduce hp by amount, but not below zero."""
        self.hp = max(0, self.hp - amount)

    def processor_i(self, amount: int) -> None:
        """Restore hp by amount, but not above max_hp."""
        self.hp = min(self.max_hp, self.hp + amount)

    def data_service(self) -> dict:
        """Serialise the common actor state to a plain dictionary."""
        return {
            "letter": self.letter,
            "name": self.name,
            "pos": list(self.pos),
            "hp": self.hp,
            "max_hp": self.max_hp,
        }

    @classmethod
    def factory_default(cls, data: dict) -> "ImplCommonProcessor":
        """Rebuild a base actor from its serialised state."""
        actor = cls(data["letter"], data["name"], tuple(data["pos"]), data["hp"])
        actor.max_hp = data["max_hp"]
        return actor
