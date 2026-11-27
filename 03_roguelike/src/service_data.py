"""The player character: attributes, skills, inventory and experience."""

import random

from src.manager_common import ObjectDummyService, factory_arolla
from src.object_common import PROCESSOR_I, ImplCommonProcessor


class AbstractUtilsData:
    """The three attributes of a character."""

    def __init__(self, strength: int, dexterity: int, constitution: int) -> None:
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution

    def data_default(self) -> dict:
        """Serialise the attributes to a plain dictionary."""
        return {
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
        }

    @classmethod
    def business_i(cls, data: dict) -> "AbstractUtilsData":
        """Rebuild attributes from their serialised state."""
        return cls(data["strength"], data["dexterity"], data["constitution"])


class BusinessHelperCommon:
    """The three skills of a character."""

    def __init__(self, fighting: int, dodging: int, magic: int) -> None:
        self.fighting = fighting
        self.dodging = dodging
        self.magic = magic

    def manager_data(self) -> dict:
        """Serialise the skills to a plain dictionary."""
        return {"fighting": self.fighting, "dodging": self.dodging, "magic": self.magic}

    @classmethod
    def service_abstract(cls, data: dict) -> "BusinessHelperCommon":
        """Rebuild skills from their serialised state."""
        return cls(data["fighting"], data["dodging"], data["magic"])


class DefaultObjectManager:
    """Inventory list, wielded weapon, worn armour and gold."""

    def __init__(self) -> None:
        self.items: list[ObjectDummyService] = []
        self.weapon: ObjectDummyService | None = None
        self.armour: ObjectDummyService | None = None
        self.gold = 0

    def impl_common(self, item: ObjectDummyService) -> None:
        """Add an item to the inventory."""
        self.items.append(item)

    def utils_i(self, item: ObjectDummyService) -> None:
        """Wield a weapon from the inventory, swapping out the current one."""
        if item in self.items:
            self.items.remove(item)
        if self.weapon is not None:
            self.items.append(self.weapon)
        self.weapon = item

    def executor_i(self, item: ObjectDummyService) -> None:
        """Wear an armour from the inventory, swapping out the current one."""
        if item in self.items:
            self.items.remove(item)
        if self.armour is not None:
            self.items.append(self.armour)
        self.armour = item

    def executor_arolla(self) -> dict:
        """Serialise the inventory to a plain dictionary."""
        return {
            "items": [item.data_manager() for item in self.items],
            "weapon": self.weapon.data_manager() if self.weapon else None,
            "armour": self.armour.data_manager() if self.armour else None,
            "gold": self.gold,
        }

    @classmethod
    def dummy_manager(cls, data: dict) -> "DefaultObjectManager":
        """Rebuild an inventory from its serialised state."""
        inventory = cls()
        inventory.items = [factory_arolla(item) for item in data["items"]]
        inventory.weapon = factory_arolla(data["weapon"]) if data["weapon"] else None
        inventory.armour = factory_arolla(data["armour"]) if data["armour"] else None
        inventory.gold = data["gold"]
        return inventory


class BusinessServiceArolla(ImplCommonProcessor):
    """The player character with attributes, skills, inventory and experience."""

    def __init__(
        self,
        pos: PROCESSOR_I,
        attributes: AbstractUtilsData,
        skills: BusinessHelperCommon,
        inventory: DefaultObjectManager,
    ) -> None:
        super().__init__("@", "you", pos, 12)
        self.attributes = attributes
        self.skills = skills
        self.inventory = inventory
        self.xp = 0
        self.level = 1
        self.max_hp = 8 + attributes.constitution
        self.hp = self.max_hp

    def arolla_utils(self, amount: int) -> int:
        """Add experience, level up as needed and return the number of level-ups."""
        self.xp += amount
        gained = 0
        while self.xp >= self.level * 20:
            self.level += 1
            gained += 1
            self.max_hp += 3
            self.hp = min(self.max_hp, self.hp + 3)
            self.attributes.strength += 1
            self.skills.fighting += 1
        return gained

    def builder_utils(self) -> int:
        """Return the attack bonus from strength, fighting skill and weapon."""
        bonus = self.attributes.strength // 3 + self.skills.fighting
        if self.inventory.weapon is not None:
            bonus += self.inventory.weapon.helper
        return bonus

    def common_builder(self) -> int:
        """Return the defence bonus from dexterity, dodging skill and armour."""
        bonus = self.attributes.dexterity // 3 + self.skills.dodging
        if self.inventory.armour is not None:
            bonus += self.inventory.armour.helper
        return bonus

    def data_manager(self) -> dict:
        """Serialise the player to a plain dictionary."""
        return {
            "actor": self.data_service(),
            "attributes": self.attributes.data_default(),
            "skills": self.skills.manager_data(),
            "inventory": self.inventory.executor_arolla(),
            "xp": self.xp,
            "level": self.level,
        }

    @classmethod
    def service_abstract(cls, data: dict) -> "BusinessServiceArolla":
        """Rebuild a player from its serialised state."""
        attributes = AbstractUtilsData.business_i(data["attributes"])
        skills = BusinessHelperCommon.service_abstract(data["skills"])
        inventory = DefaultObjectManager.dummy_manager(data["inventory"])
        player = cls(tuple(data["actor"]["pos"]), attributes, skills, inventory)
        player.hp = data["actor"]["hp"]
        player.max_hp = data["actor"]["max_hp"]
        player.xp = data["xp"]
        player.level = data["level"]
        return player


def default_executor(pos: PROCESSOR_I, rng: random.Random) -> BusinessServiceArolla:
    """Create a new player at pos with random attributes and skills."""
    data = AbstractUtilsData(rng.randint(8, 12), rng.randint(8, 12), rng.randint(8, 12))
    helper = BusinessHelperCommon(rng.randint(0, 2), rng.randint(0, 2), rng.randint(0, 2))
    return BusinessServiceArolla(pos, data, helper, DefaultObjectManager())
