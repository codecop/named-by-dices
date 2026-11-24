#include "helper_abstract_data.h"

#include <stdlib.h>

default_builder_impl executor_common_helper(int object) {
    switch (object) {
        case 'w':
            return PROCESSOR_AROLLA_MANAGER;
        case 'a':
            return UTILS_BUILDER_ABSTRACT;
        case 's':
            return SERVICE_COMMON_PROCESSOR;
        case 'd':
            return AROLLA_DATA_SERVICE;
        default:
            return AROLLA_IMPL_EXECUTOR;
    }
}

int dummy_business_impl(factory_arolla_object *object, const abstract_utils_object *dummy, helper_object_default helper, void *manager) {
    int service = builder_helper_i(object);
    char *utils = (char *)malloc((size_t)service);
    while (abstract_executor_impl(object) == BUSINESS_SERVICE_I) {
        int factory;
        dummy_business_manager(object, utils, service);
        dummy->impl(dummy->data);
        dummy->factory(dummy->data, utils);
        dummy->helper(dummy->data, DATA_FACTORY_AROLLA);
        factory = dummy->utils(dummy->data);
        if (factory == 'q') {
            break;
        }
        i_utils_builder(object, executor_common_helper(factory), helper, manager);
    }
    dummy_business_manager(object, utils, service);
    dummy->impl(dummy->data);
    dummy->factory(dummy->data, utils);
    free(utils);
    return (int)abstract_executor_impl(object);
}
