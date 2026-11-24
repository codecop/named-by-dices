#include "data_utils_arolla.h"

static void executor_impl_default(factory_arolla_object *object) {
    int i;
    object->utils.utils.data = builder_utils_dummy(object->data);
    object->utils.utils.common = utils_business_arolla(object->data);
    object->utils.factory = PROCESSOR_AROLLA_MANAGER;
    object->utils.helper = AROLLA_IMPL_EXECUTOR;
    for (i = 0; i < UTILS_AROLLA_EXECUTOR; i++) {
        processor_abstract_impl dummy = { service_data_common(object->data, i), business_i_helper(object->data, i) };
        object->factory[i] = arolla_data_helper(dummy, UTILS_BUILDER_ABSTRACT);
    }
}

void business_dummy_manager(factory_arolla_object *object, builder_helper_arolla *dummy) {
    object->data = dummy;
    processor_i_manager(dummy);
    executor_impl_default(object);
    object->common = 0;
    object->helper = IMPL_I_PROCESSOR;
    object->impl = builder_i_factory(dummy);
    object->manager = 0;
    object->service = BUSINESS_SERVICE_I;
}

static void manager_executor_dummy(factory_arolla_object *object) {
    int data = object->utils.utils.data;
    int common = object->utils.utils.common;
    char utils = builder_i_manager(object->data, data, common);
    if (utils == COMMON_BUILDER_IMPL) {
        object->common += FACTORY_OBJECT_ABSTRACT;
        object->impl--;
        data_helper_i(object->data, data, common, OBJECT_I_IMPL);
    } else if (utils == OBJECT_COMMON_HELPER) {
        int i;
        object->common += BUILDER_AROLLA_SERVICE;
        object->impl--;
        data_helper_i(object->data, data, common, OBJECT_I_IMPL);
        for (i = 0; i < UTILS_AROLLA_EXECUTOR; i++) {
            object->factory[i].helper = AROLLA_BUSINESS_HELPER;
            object->factory[i].data = OBJECT_COMMON_MANAGER;
        }
    }
}

static void helper_arolla_processor(factory_arolla_object *object, int data) {
    executor_default_service *dummy = &object->factory[data];
    if (dummy->helper == AROLLA_BUSINESS_HELPER) {
        object->common += UTILS_AROLLA_PROCESSOR;
        dummy->utils = dummy->common;
        dummy->factory = PROCESSOR_AROLLA_MANAGER;
        dummy->helper = HELPER_I_BUILDER;
        dummy->data = 0;
    } else {
        object->helper--;
        if (object->helper <= 0) {
            object->service = EXECUTOR_DUMMY_IMPL;
        } else {
            executor_impl_default(object);
        }
    }
}

void i_utils_builder(factory_arolla_object *object, default_builder_impl dummy, helper_object_default helper, void *manager) {
    processor_abstract_impl utils;
    int i;
    if (object->service != BUSINESS_SERVICE_I) {
        return;
    }
    if (dummy != AROLLA_IMPL_EXECUTOR) {
        processor_abstract_impl factory = i_impl_object(object->utils.utils, dummy);
        if (default_factory_processor(object->data, factory.data, factory.common)) {
            object->utils.factory = dummy;
        }
    }
    object->utils.helper = dummy;
    utils = i_impl_object(object->utils.utils, object->utils.factory);
    if (default_factory_processor(object->data, utils.data, utils.common)) {
        object->utils.utils = utils;
    }
    manager_executor_dummy(object);
    object->manager++;
    if (object->manager % 2 == 0) {
        for (i = 0; i < UTILS_AROLLA_EXECUTOR; i++) {
            executor_default_service *arolla = &object->factory[i];
            int common = 0;
            default_builder_impl impl;
            processor_abstract_impl processor;
            if (arolla->helper == AROLLA_BUSINESS_HELPER && arolla->data > 0) {
                arolla->data--;
                if (arolla->data == 0) {
                    arolla->helper = HELPER_I_BUILDER;
                }
                common = 1;
            }
            impl = object_helper_dummy(object->data, arolla, object->utils.utils, common, helper, manager);
            processor = i_impl_object(arolla->utils, impl);
            if (object_manager_common(object->data, processor.data, processor.common)) {
                arolla->utils = processor;
                arolla->factory = impl;
            }
        }
    }
    for (i = 0; i < UTILS_AROLLA_EXECUTOR; i++) {
        executor_default_service *arolla = &object->factory[i];
        if (arolla->utils.data == object->utils.utils.data && arolla->utils.common == object->utils.utils.common) {
            helper_arolla_processor(object, i);
            break;
        }
    }
    if (object->service == BUSINESS_SERVICE_I && object->impl == 0) {
        object->service = AROLLA_IMPL_BUSINESS;
    }
}

builder_default_factory abstract_executor_impl(const factory_arolla_object *object) {
    return object->service;
}

int object_default_factory(const factory_arolla_object *object) {
    return object->common;
}

int abstract_impl_data(const factory_arolla_object *object) {
    return object->helper;
}

int default_processor_utils(const factory_arolla_object *object) {
    return object->impl;
}

business_manager_arolla dummy_factory_executor(const factory_arolla_object *object) {
    return object->utils;
}

const executor_default_service * data_arolla_factory(const factory_arolla_object *object, int data) {
    return &object->factory[data];
}

const builder_helper_arolla * abstract_utils_builder(const factory_arolla_object *object) {
    return object->data;
}
