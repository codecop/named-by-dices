#ifndef DATA_COMMON_MANAGER
#define DATA_COMMON_MANAGER

typedef enum {
    PROCESSOR_AROLLA_MANAGER,
    UTILS_BUILDER_ABSTRACT,
    SERVICE_COMMON_PROCESSOR,
    AROLLA_DATA_SERVICE,
    AROLLA_IMPL_EXECUTOR
} default_builder_impl;

typedef struct {
    int data;
    int common;
} processor_abstract_impl;

typedef struct {
    processor_abstract_impl utils;
    default_builder_impl factory;
    default_builder_impl helper;
} business_manager_arolla;

typedef unsigned (*helper_object_default)(void *);

int manager_executor_abstract(default_builder_impl object);
int helper_i_processor(default_builder_impl object);
processor_abstract_impl i_impl_object(processor_abstract_impl object, default_builder_impl dummy);
default_builder_impl helper_data_i(default_builder_impl object);

#endif
