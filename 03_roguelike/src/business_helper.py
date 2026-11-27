UTILS_PROCESSOR = {
    "#": "\x1b[90m#\x1b[0m",
    "+": "\x1b[33m+\x1b[0m",
    ">": "\x1b[97m>\x1b[0m",
    "<": "\x1b[97m<\x1b[0m",
}


def service_dummy(impl) -> str:
    factory = impl.factory
    common = (
        f"Str {factory.builder.builder} Dex {factory.builder.business} "
        f"Con {factory.builder.common}"
    )
    default = (
        f"Fight {factory.business.data} Dodge {factory.business.helper} "
        f"Magic {factory.business.service}"
    )
    return (
        f"HP {factory.helper}/{factory.factory}  Lvl {factory.arolla}  "
        f"XP {factory.abstract}  {common}  {default}  Gold {factory.common.service}  "
        f"Depth {impl.business.data}/{impl.common.helper.data}  "
        f"Atk {factory.builder_utils()} Def {factory.common_builder()}"
    )


def object_impl(helper, data, executor):
    manager = helper.object.factory.get(data)
    if manager is not None and data in executor:
        common = "\x1b[92m" if manager.processor else "\x1b[91m"
        return common + manager.impl + "\x1b[0m"
    service = helper.object.helper.get(data)
    if service is not None and data in executor:
        return "\x1b[96m" + service.impl + "\x1b[0m"
    processor = helper.object.impl.get(data)
    if processor is not None and processor.helper and data in executor:
        return "\x1b[31m^\x1b[0m"
    return None


def utils_i(helper, data, executor) -> str:
    factory = helper.utils_data(data)
    if data in executor:
        return UTILS_PROCESSOR.get(factory, factory)
    if data in helper.object.service:
        return "\x1b[2m" + factory + "\x1b[0m"
    return " "


def i_business(helper, data, factory, executor) -> str:
    if data == factory.data:
        return "\x1b[93m@\x1b[0m"
    common = object_impl(helper, data, executor)
    if common is not None:
        return common
    return utils_i(helper, data, executor)


def helper_i(helper, factory, executor) -> list[str]:
    manager = []
    for service in range(helper.executor.default):
        impl = []
        for builder in range(helper.executor.common):
            impl.append(i_business(helper, (builder, service), factory, executor))
        manager.append("".join(impl))
    return manager


def utils_default(impl) -> str:
    helper = impl.business.helper_i()
    manager = [service_dummy(impl)]
    manager.extend(helper_i(helper, impl.factory, impl.executor))
    if impl.abstract.helper:
        manager.append(impl.abstract.service)
        manager.append("*** YOU WIN ***  press Q to quit")
    else:
        manager.append(impl.abstract.service)
    return "\x1b[2J\x1b[H" + "\n".join(manager)
