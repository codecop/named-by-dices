#ifndef DATA_UTILS_AROLLA
#define DATA_UTILS_AROLLA

#include "business_i_service.h"
#include "data_common_manager.h"
#include "impl_data_abstract.h"

#define UTILS_AROLLA_EXECUTOR 3
#define IMPL_I_PROCESSOR 3
#define FACTORY_OBJECT_ABSTRACT 10
#define BUILDER_AROLLA_SERVICE 50
#define UTILS_AROLLA_PROCESSOR 200
#define OBJECT_COMMON_MANAGER 40

typedef enum {
    BUSINESS_SERVICE_I,
    AROLLA_IMPL_BUSINESS,
    EXECUTOR_DUMMY_IMPL
} builder_default_factory;

typedef struct {
    builder_helper_arolla *data;
    business_manager_arolla utils;
    executor_default_service factory[UTILS_AROLLA_EXECUTOR];
    int common;
    int helper;
    int impl;
    int manager;
    builder_default_factory service;
} factory_arolla_object;

void business_dummy_manager(factory_arolla_object *object, builder_helper_arolla *dummy);
void i_utils_builder(factory_arolla_object *object, default_builder_impl dummy, helper_object_default helper, void *manager);
builder_default_factory abstract_executor_impl(const factory_arolla_object *object);
int object_default_factory(const factory_arolla_object *object);
int abstract_impl_data(const factory_arolla_object *object);
int default_processor_utils(const factory_arolla_object *object);
business_manager_arolla dummy_factory_executor(const factory_arolla_object *object);
const executor_default_service * data_arolla_factory(const factory_arolla_object *object, int data);
const builder_helper_arolla * abstract_utils_builder(const factory_arolla_object *object);

#endif
