#ifndef IMPL_DATA_ABSTRACT
#define IMPL_DATA_ABSTRACT

#include "business_i_service.h"
#include "data_common_manager.h"

typedef enum {
    HELPER_I_BUILDER,
    AROLLA_BUSINESS_HELPER
} arolla_factory_processor;

typedef struct {
    processor_abstract_impl utils;
    processor_abstract_impl common;
    default_builder_impl factory;
    arolla_factory_processor helper;
    int data;
} executor_default_service;

executor_default_service arolla_data_helper(processor_abstract_impl object, default_builder_impl dummy);
default_builder_impl object_helper_dummy(const builder_helper_arolla *object, const executor_default_service *dummy, processor_abstract_impl helper, int manager, helper_object_default service, void *executor);

#endif
