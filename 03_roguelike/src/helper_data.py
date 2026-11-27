from src.data_common import UtilsCommonExecutor
from src.object_common import PROCESSOR_I, i_data


def builder_utils(
    executor: UtilsCommonExecutor, data: PROCESSOR_I, helper: PROCESSOR_I
) -> bool:
    common = data
    default = helper
    factory = abs(default[0] - common[0])
    impl = abs(default[1] - common[1])
    utils = 1 if default[0] >= common[0] else -1
    processor = 1 if default[1] >= common[1] else -1
    manager = factory - impl
    builder = common[0]
    business = common[1]
    dummy = 0
    while (builder, business) != default and dummy < 1000:
        dummy += 1
        service = (builder, business)
        if service not in (data, helper) and executor.factory_default(service):
            return False
        abstract = 2 * manager
        if abstract >= -impl:
            manager -= impl
            builder += utils
        if abstract <= factory:
            manager += factory
            business += processor
    return True


def arolla_utils(
    executor: UtilsCommonExecutor, origin: PROCESSOR_I, data: int
) -> set[PROCESSOR_I]:
    impl = {origin}
    for helper in range(max(0, origin[1] - data), min(executor.default, origin[1] + data + 1)):
        for service in range(
            max(0, origin[0] - data), min(executor.common, origin[0] + data + 1)
        ):
            common = (service, helper)
            if (
                i_data(origin, common) <= data
                and not executor.factory_default(common)
                and builder_utils(executor, origin, common)
            ):
                impl.add(common)
    return impl
