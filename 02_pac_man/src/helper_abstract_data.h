#ifndef HELPER_ABSTRACT_DATA
#define HELPER_ABSTRACT_DATA

#include "object_abstract_helper.h"

#define DATA_FACTORY_AROLLA 120

typedef struct {
    void *data;
    int (*utils)(void *);
    void (*factory)(void *, const char *);
    void (*helper)(void *, int);
    void (*impl)(void *);
} abstract_utils_object;

default_builder_impl executor_common_helper(int object);
int dummy_business_impl(factory_arolla_object *object, const abstract_utils_object *dummy, helper_object_default helper, void *manager);
void common_processor(int object, const abstract_utils_object *dummy);
unsigned executor_arolla(void *object);

#endif
