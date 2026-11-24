#include "impl_data_abstract.h"

static int arolla_processor_impl(processor_abstract_impl object, processor_abstract_impl dummy) {
    int data = object.data - dummy.data;
    int common = object.common - dummy.common;
    if (data < 0) {
        data = -data;
    }
    if (common < 0) {
        common = -common;
    }
    return data + common;
}

executor_default_service arolla_data_helper(processor_abstract_impl object, default_builder_impl dummy) {
    executor_default_service helper;
    helper.utils = object;
    helper.common = object;
    helper.factory = dummy;
    helper.helper = HELPER_I_BUILDER;
    helper.data = 0;
    return helper;
}

default_builder_impl object_helper_dummy(const builder_helper_arolla *object, const executor_default_service *dummy, processor_abstract_impl helper, int manager, helper_object_default service, void *executor) {
    static const default_builder_impl utils[] = { PROCESSOR_AROLLA_MANAGER, UTILS_BUILDER_ABSTRACT, SERVICE_COMMON_PROCESSOR, AROLLA_DATA_SERVICE };
    default_builder_impl arolla[4];
    default_builder_impl reverse = helper_data_i(dummy->factory);
    default_builder_impl best;
    int data = 0;
    int common = 0;
    int i;
    for (i = 0; i < 4; i++) {
        processor_abstract_impl processor;
        if (utils[i] == reverse && dummy->factory != AROLLA_IMPL_EXECUTOR) {
            continue;
        }
        processor = i_impl_object(dummy->utils, utils[i]);
        if (object_manager_common(object, processor.data, processor.common)) {
            arolla[data] = utils[i];
            data++;
        }
    }
    if (data == 0) {
        return reverse;
    }
    if (manager) {
        return arolla[service(executor) % (unsigned)data];
    }
    best = arolla[0];
    common = arolla_processor_impl(i_impl_object(dummy->utils, arolla[0]), helper);
    for (i = 1; i < data; i++) {
        processor_abstract_impl impl = i_impl_object(dummy->utils, arolla[i]);
        int factory = arolla_processor_impl(impl, helper);
        if (factory < common) {
            common = factory;
            best = arolla[i];
        }
    }
    return best;
}
