#include "data_common_manager.h"

int manager_executor_abstract(default_builder_impl object) {
    if (object == UTILS_BUILDER_ABSTRACT) {
        return -1;
    }
    if (object == AROLLA_DATA_SERVICE) {
        return 1;
    }
    return 0;
}

int helper_i_processor(default_builder_impl object) {
    if (object == PROCESSOR_AROLLA_MANAGER) {
        return -1;
    }
    if (object == SERVICE_COMMON_PROCESSOR) {
        return 1;
    }
    return 0;
}

processor_abstract_impl i_impl_object(processor_abstract_impl object, default_builder_impl dummy) {
    processor_abstract_impl utils = object;
    utils.data += manager_executor_abstract(dummy);
    utils.common += helper_i_processor(dummy);
    return utils;
}

default_builder_impl helper_data_i(default_builder_impl object) {
    switch (object) {
        case PROCESSOR_AROLLA_MANAGER:
            return SERVICE_COMMON_PROCESSOR;
        case SERVICE_COMMON_PROCESSOR:
            return PROCESSOR_AROLLA_MANAGER;
        case UTILS_BUILDER_ABSTRACT:
            return AROLLA_DATA_SERVICE;
        case AROLLA_DATA_SERVICE:
            return UTILS_BUILDER_ABSTRACT;
        default:
            return AROLLA_IMPL_EXECUTOR;
    }
}
