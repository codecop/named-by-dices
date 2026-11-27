"""Dungeon items: weapons, armour, potions, scrolls, wands, gold and the artefact."""

import random

FACTORY_DUMMY = {
    "weapon": [
        (")", "dagger", 1),
        (")", "short sword", 2),
        (")", "battle axe", 3),
        (")", "magic blade", 5),
    ],
    "armour": [("[", "leather armour", 1), ("[", "chain mail", 2)],
    "potion": [
        ("!", "healing potion", 6),
        ("!", "greater healing potion", 12),
        ("!", "poison", -4),
    ],
    "scroll": [
        ("?", "scroll of magic mapping", 0),
        ("?", "scroll of teleportation", 0),
        ("?", "scroll of fireball", 8),
    ],
    "wand": [("/", "wand of magic missile", 5)],
    "gold": [("$", "pile of gold", 0)],
}


class ObjectDummyService:
    """One dungeon item; kind is one of weapon, armour, potion, scroll, wand, gold, artefact."""

    def __init__(
        self, impl: str, service: str, data: str, helper: int, factory: int = 0
    ) -> None:
        self.impl = impl
        self.service = service
        self.data = data
        self.helper = helper
        self.factory = factory

    def manager_abstract(self) -> str:
        """Return the display name of the item."""
        return self.service

    def data_manager(self) -> dict:
        """Serialise the item to a plain dictionary."""
        return {
            "letter": self.impl,
            "name": self.service,
            "kind": self.data,
            "power": self.helper,
            "charges": self.factory,
        }

    @classmethod
    def service_abstract(cls, data: dict) -> "ObjectDummyService":
        """Rebuild an item from its serialised state."""
        return cls(data["letter"], data["name"], data["kind"], data["power"], data["charges"])


def executor_factory(rng: random.Random, depth: int) -> ObjectDummyService:
    """Create a random item; weapons, armour and gold scale with the dungeon depth."""
    data = rng.choice(
        ("weapon", "armour", "potion", "potion", "scroll", "wand", "gold", "gold")
    )
    helper, service, utils = rng.choice(FACTORY_DUMMY[data])
    if data in ("weapon", "armour"):
        utils += depth // 2
    elif data == "gold":
        utils = rng.randint(10, 30) * depth
    factory = utils if data == "wand" else 0
    return ObjectDummyService(helper, service, data, utils, factory)


def factory_arolla(data: dict) -> ObjectDummyService:
    """Rebuild an item from its serialised state."""
    return ObjectDummyService.service_abstract(data)


def object_arolla() -> ObjectDummyService:
    """Create the unique artefact, the Golden Die, hidden on the deepest level."""
    return ObjectDummyService("&", "the Golden Die", "artefact", 0)
