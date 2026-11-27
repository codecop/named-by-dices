UTILS_PROCESSOR = {
    "#": "\x1b[90m#\x1b[0m",
    "+": "\x1b[33m+\x1b[0m",
    ">": "\x1b[97m>\x1b[0m",
    "<": "\x1b[97m<\x1b[0m",
}


def service_dummy(game) -> str:
    player = game.player
    stats = (
        f"Str {player.builder.builder} Dex {player.builder.business} "
        f"Con {player.builder.common}"
    )
    skills = (
        f"Fight {player.business.data} Dodge {player.business.helper} "
        f"Magic {player.business.service}"
    )
    return (
        f"HP {player.helper}/{player.factory}  Lvl {player.arolla}  XP {player.abstract}  "
        f"{stats}  {skills}  Gold {player.common.service}  "
        f"Depth {game.world.data}/{game.config.helper.data}  "
        f"Atk {player.builder_utils()} Def {player.common_builder()}"
    )


def object_impl(level, pos, visible):
    monster = level.object.factory.get(pos)
    if monster is not None and pos in visible:
        colour = "\x1b[92m" if monster.processor else "\x1b[91m"
        return colour + monster.impl + "\x1b[0m"
    item = level.object.helper.get(pos)
    if item is not None and pos in visible:
        return "\x1b[96m" + item.impl + "\x1b[0m"
    trap = level.object.impl.get(pos)
    if trap is not None and trap.helper and pos in visible:
        return "\x1b[31m^\x1b[0m"
    return None


def utils_i(level, pos, visible) -> str:
    tile = level.utils_data(pos)
    if pos in visible:
        return UTILS_PROCESSOR.get(tile, tile)
    if pos in level.object.service:
        return "\x1b[2m" + tile + "\x1b[0m"
    return " "


def i_business(level, pos, player, visible) -> str:
    if pos == player.data:
        return "\x1b[93m@\x1b[0m"
    entity = object_impl(level, pos, visible)
    if entity is not None:
        return entity
    return utils_i(level, pos, visible)


def helper_i(level, player, visible) -> list[str]:
    rows = []
    for yy in range(level.executor.default):
        data = []
        for xx in range(level.executor.common):
            data.append(i_business(level, (xx, yy), player, visible))
        rows.append("".join(data))
    return rows


def utils_default(game) -> str:
    level = game.world.helper_i()
    lines = [service_dummy(game)]
    lines.extend(helper_i(level, game.player, game.visible))
    if game.status.helper:
        lines.append(game.status.service)
        lines.append("*** YOU WIN ***  press Q to quit")
    else:
        lines.append(game.status.service)
    return "\x1b[2J\x1b[H" + "\n".join(lines)
