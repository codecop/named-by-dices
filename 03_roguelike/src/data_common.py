"""Seeded dungeon generation: rooms, corridors, doors, stairs and traps."""

import random

from src.object_common import PROCESSOR_I, builder_default

BUSINESS_COMMON = 78
COMMON_UTILS = 22
DEFAULT_MANAGER = 8
DUMMY_MANAGER = 5
EXECUTOR_AROLLA = 10
FACTORY_PROCESSOR = 14


class ArollaImplData:
    """A rectangular room on a dungeon level."""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def utils_common(self) -> PROCESSOR_I:
        """Return the centre cell of the room."""
        return (self.x + self.width // 2, self.y + self.height // 2)

    def impl_builder(self, other: "ArollaImplData") -> bool:
        """Return whether this room overlaps other, including one cell of padding."""
        return not (
            self.x + self.width + 1 < other.x
            or other.x + other.width + 1 < self.x
            or self.y + self.height + 1 < other.y
            or other.y + other.height + 1 < self.y
        )

    def object_default(self, pos: PROCESSOR_I) -> bool:
        """Return whether pos lies inside the room rectangle."""
        return (
            self.x <= pos[0] < self.x + self.width
            and self.y <= pos[1] < self.y + self.height
        )

    def processor_factory(self, rng: random.Random) -> PROCESSOR_I:
        """Return a random interior cell of the room."""
        return (
            rng.randint(self.x + 1, self.x + self.width - 2),
            rng.randint(self.y + 1, self.y + self.height - 2),
        )

    def service_dummy(self) -> list[PROCESSOR_I]:
        """Return the perimeter cells of the room rectangle."""
        cells = []
        for xx in range(self.x, self.x + self.width):
            cells.append((xx, self.y))
            cells.append((xx, self.y + self.height - 1))
        for yy in range(self.y + 1, self.y + self.height - 1):
            cells.append((self.x, yy))
            cells.append((self.x + self.width - 1, yy))
        return cells

    def manager_object(self) -> dict:
        """Serialise the room to a plain dictionary."""
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}

    @classmethod
    def data_arolla(cls, data: dict) -> "ArollaImplData":
        """Rebuild a room from its serialised state."""
        return cls(data["x"], data["y"], data["width"], data["height"])


class ImplProcessorDefault:
    """A trap hidden in the dungeon floor until it is found or triggered."""

    FACTORY_DEFAULT = ("dart", "teleport", "alarm")

    def __init__(self, kind: str, found: bool = False) -> None:
        self.kind = kind
        self.found = found

    def object_factory(self) -> dict:
        """Serialise the trap to a plain dictionary."""
        return {"kind": self.kind, "found": self.found}

    @classmethod
    def i_utils(cls, data: dict) -> "ImplProcessorDefault":
        """Rebuild a trap from its serialised state."""
        return cls(data["kind"], data["found"])


class UtilsCommonExecutor:
    """The tile grid of one dungeon level."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [["#"] * width for _ in range(height)]

    def utils_data(self, pos: PROCESSOR_I) -> str:
        """Return the tile character at pos, '#' when out of bounds."""
        if not self.i_business(pos):
            return "#"
        return self.grid[pos[1]][pos[0]]

    def helper_executor(self, pos: PROCESSOR_I, tile: str) -> None:
        """Set the tile character at pos."""
        self.grid[pos[1]][pos[0]] = tile

    def factory_default(self, pos: PROCESSOR_I) -> bool:
        """Return whether pos is a wall or outside the grid."""
        return self.utils_data(pos) == "#"

    def i_business(self, pos: PROCESSOR_I) -> bool:
        """Return whether pos lies inside the grid."""
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def impl_dummy(self, pos: PROCESSOR_I) -> bool:
        """Return whether pos is walkable: inside the grid and not a wall."""
        return self.i_business(pos) and not self.factory_default(pos)

    def executor_arolla(self) -> dict:
        """Serialise the grid to a plain dictionary."""
        return {
            "width": self.width,
            "height": self.height,
            "grid": ["".join(row) for row in self.grid],
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "UtilsCommonExecutor":
        """Rebuild a grid from its serialised state."""
        grid = cls(data["width"], data["height"])
        grid.grid = [list(row) for row in data["grid"]]
        return grid


class ServiceObjectCommon:
    """Monsters, items, traps and explored cells living on one level."""

    def __init__(self) -> None:
        self.monsters: dict[PROCESSOR_I, object] = {}
        self.items: dict[PROCESSOR_I, object] = {}
        self.traps: dict[PROCESSOR_I, ImplProcessorDefault] = {}
        self.explored: set[PROCESSOR_I] = set()

    def business_arolla(
        self,
        grid: UtilsCommonExecutor,
        rng: random.Random,
        avoid: tuple = (),
        fallback: PROCESSOR_I | None = None,
    ) -> PROCESSOR_I | None:
        """Return a random walkable cell free of items and monsters."""
        for _ in range(200):
            cell = (rng.randrange(1, grid.width - 1), rng.randrange(1, grid.height - 1))
            if (
                grid.impl_dummy(cell)
                and cell not in avoid
                and cell not in self.items
                and cell not in self.monsters
            ):
                return cell
        return fallback

    def executor_arolla(self) -> dict:
        """Serialise traps and explored cells; the game serialises monsters and items."""
        return {
            "traps": [
                {"pos": list(pos), **trap.object_factory()}
                for pos, trap in self.traps.items()
            ],
            "explored": [list(cell) for cell in sorted(self.explored)],
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "ServiceObjectCommon":
        """Rebuild the entity layer from its serialised state."""
        layer = cls()
        layer.traps = {
            tuple(trap["pos"]): ImplProcessorDefault.i_utils(trap) for trap in data["traps"]
        }
        layer.explored = {tuple(cell) for cell in data["explored"]}
        return layer


class ManagerBusinessArolla:
    """One dungeon level composing the tile grid, the entity layer, rooms and stairs."""

    def __init__(self, width: int, height: int, depth: int) -> None:
        self.grid = UtilsCommonExecutor(width, height)
        self.entities = ServiceObjectCommon()
        self.depth = depth
        self.rooms: list[ArollaImplData] = []
        self.stairs_down: PROCESSOR_I | None = None
        self.stairs_up: PROCESSOR_I | None = None

    def utils_data(self, pos: PROCESSOR_I) -> str:
        """Return the tile character at pos, '#' when out of bounds."""
        return self.grid.utils_data(pos)

    def helper_executor(self, pos: PROCESSOR_I, tile: str) -> None:
        """Set the tile character at pos."""
        self.grid.helper_executor(pos, tile)

    def factory_default(self, pos: PROCESSOR_I) -> bool:
        """Return whether pos is a wall or outside the grid."""
        return self.grid.factory_default(pos)

    def i_business(self, pos: PROCESSOR_I) -> bool:
        """Return whether pos lies inside the grid."""
        return self.grid.i_business(pos)

    def impl_dummy(self, pos: PROCESSOR_I) -> bool:
        """Return whether pos is walkable: inside the grid and not a wall."""
        return self.grid.impl_dummy(pos)

    def business_arolla(self, rng: random.Random, avoid: tuple = ()) -> PROCESSOR_I:
        """Return a random walkable cell free of items and monsters on this level."""
        fallback = self.rooms[0].utils_common if self.rooms else (1, 1)
        cell = self.entities.business_arolla(self.grid, rng, avoid, fallback)
        return cell if cell is not None else fallback

    def executor_arolla(self) -> dict:
        """Serialise the level to a plain dictionary; the game adds monsters and items."""
        return {
            "depth": self.depth,
            "grid": self.grid.executor_arolla(),
            "entities": self.entities.executor_arolla(),
            "rooms": [room.manager_object() for room in self.rooms],
            "stairs_down": list(self.stairs_down) if self.stairs_down else None,
            "stairs_up": list(self.stairs_up) if self.stairs_up else None,
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "ManagerBusinessArolla":
        """Rebuild a level from its serialised state."""
        level = cls(data["grid"]["width"], data["grid"]["height"], data["depth"])
        level.grid = UtilsCommonExecutor.dummy_manager(data["grid"])
        level.entities = ServiceObjectCommon.dummy_manager(data["entities"])
        level.rooms = [ArollaImplData.data_arolla(room) for room in data["rooms"]]
        level.stairs_down = tuple(data["stairs_down"]) if data["stairs_down"] else None
        level.stairs_up = tuple(data["stairs_up"]) if data["stairs_up"] else None
        return level


def data_service(rng: random.Random, depth: int) -> ManagerBusinessArolla:
    """Generate one seed-dependent dungeon level with at least ten rooms."""
    level = ManagerBusinessArolla(BUSINESS_COMMON, COMMON_UTILS, depth)
    count = rng.randint(EXECUTOR_AROLLA, FACTORY_PROCESSOR)
    i_impl(level, rng, count)
    impl_business(level, rng)
    common_helper(level)
    processor_manager(level, rng)
    utils_executor(level, rng)
    return level


def i_impl(level: ManagerBusinessArolla, rng: random.Random, count: int) -> None:
    """Place up to count non-overlapping rooms and carve their floors."""
    attempts = 0
    while len(level.rooms) < count and attempts < 500:
        attempts += 1
        width = rng.randint(4, 10)
        height = rng.randint(3, 7)
        x = rng.randint(1, level.grid.width - width - 2)
        y = rng.randint(1, level.grid.height - height - 2)
        room = ArollaImplData(x, y, width, height)
        if any(room.impl_builder(other) for other in level.rooms):
            continue
        level.rooms.append(room)
        for yy in range(y, y + height):
            for xx in range(x, x + width):
                level.helper_executor((xx, yy), ".")


def impl_business(level: ManagerBusinessArolla, rng: random.Random) -> None:
    """Connect consecutive room centres with L-shaped corridors, plus one loop."""
    rooms = level.rooms
    for index in range(len(rooms) - 1):
        i_service(level, rooms[index].utils_common, rooms[index + 1].utils_common, rng)
    if len(rooms) > 3:
        index = rng.randrange(len(rooms) - 2)
        i_service(level, rooms[index].utils_common, rooms[index + 2].utils_common, rng)


def i_service(
    level: ManagerBusinessArolla,
    a: PROCESSOR_I,
    b: PROCESSOR_I,
    rng: random.Random,
) -> None:
    """Carve an L-shaped corridor between a and b, horizontal first or vertical first."""
    if rng.random() < 0.5:
        abstract_processor(level, a[0], a[1], b[0], a[1])
        abstract_processor(level, b[0], a[1], b[0], b[1])
    else:
        abstract_processor(level, a[0], a[1], a[0], b[1])
        abstract_processor(level, a[0], b[1], b[0], b[1])


def abstract_processor(
    level: ManagerBusinessArolla, x1: int, y1: int, x2: int, y2: int
) -> None:
    """Carve a straight horizontal or vertical line of floor."""
    if y1 == y2:
        for xx in range(min(x1, x2), max(x1, x2) + 1):
            level.helper_executor((xx, y1), ".")
    else:
        for yy in range(min(y1, y2), max(y1, y2) + 1):
            level.helper_executor((x1, yy), ".")


def common_helper(level: ManagerBusinessArolla) -> None:
    """Mark room border cells that connect to a corridor as doors."""
    for room in level.rooms:
        for cell in room.service_dummy():
            if level.utils_data(cell) != ".":
                continue
            outside = [
                neighbour
                for neighbour in builder_default(cell)
                if level.impl_dummy(neighbour) and not room.object_default(neighbour)
            ]
            if outside:
                level.helper_executor(cell, "+")


def processor_manager(level: ManagerBusinessArolla, rng: random.Random) -> None:
    """Place up stairs on the first level and down stairs on all but the last level."""
    start = level.rooms[0]
    if level.depth == 1:
        level.stairs_up = start.processor_factory(rng)
        level.helper_executor(level.stairs_up, "<")
    if level.depth < DUMMY_MANAGER:
        room = rng.choice(level.rooms[1:])
        cell = room.processor_factory(rng)
        guard = 0
        while cell == level.stairs_up and guard < 20:
            cell = room.processor_factory(rng)
            guard += 1
        level.stairs_down = cell
        level.helper_executor(cell, ">")


def utils_executor(level: ManagerBusinessArolla, rng: random.Random) -> None:
    """Place a handful of hidden traps on random floor cells outside the start room."""
    count = rng.randint(3, 6)
    start = level.rooms[0]
    placed = 0
    attempts = 0
    while placed < count and attempts < 200:
        attempts += 1
        cell = level.business_arolla(rng, avoid=(level.stairs_down, level.stairs_up))
        if start.object_default(cell) or cell in level.entities.traps:
            continue
        kind = rng.choice(ImplProcessorDefault.FACTORY_DEFAULT)
        level.entities.traps[cell] = ImplProcessorDefault(kind)
        placed += 1
