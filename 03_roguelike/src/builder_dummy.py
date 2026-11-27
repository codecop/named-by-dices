def business_abstract() -> list[str]:
    return [
        "THE CAVERNS OF DICE",
        "",
        "A dragon has stolen the Golden Die, the artefact of the dicesmiths,",
        "and hidden it in the deepest cavern.",
        "Descend, fight, loot, and bring it back to the surface.",
        "",
        "Keys: hjkl/yubn move, . rest, > descend, < ascend, , pick up,",
        "i inventory, w wield, W wear, q quaff, r read, z zap,",
        "s save game, Q quit, ? help",
    ]


def helper_arolla(data: int) -> str:
    common = {
        1: "You enter the Caverns of Dice.",
        2: "The air grows cold and damp.",
        3: "Something big snores in the dark...",
        4: "The stench of dragon approaches.",
        5: "The deepest hall. The Golden Die glitters on its pedestal.",
    }
    return common.get(data, f"Depth {data}.")


def impl_common(data: str) -> str:
    common = {
        "dragon": "The dragon awakens and roars!",
        "amulet": "You take the Golden Die! Now get out alive!",
        "win": "You emerge from the caverns with the Golden Die. You win!",
        "death": "You die in the dark... Game over.",
    }
    return common.get(data, "")
