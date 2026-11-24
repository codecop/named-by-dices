#include "business_i_service.h"

#include <stdlib.h>
#include <string.h>

static const char * const arolla_processor_service[] = {
    "#####################",
    "#.........#.........#",
    "#o.##.###.#.###.##.o#",
    "#...................#",
    "#.##.#.#######.#.##.#",
    "#....#.........#....#",
    "####.###.#.###.######",
    "#.......##-##.......#",
    "#.......#GGG#.......#",
    "#.......#####.......#",
    "#.##.#.#####.#.##.#.#",
    "#o.#......P......#.o#",
    "#.#####.#.#####.#.#.#",
    "#.........#.........#",
    "#####################"
};

static builder_helper_arolla dummy_data_impl;
static int i_service_processor;

void i_processor_helper(builder_helper_arolla *object, const char * const *dummy, int helper) {
    int i;
    object->data = (int)strlen(dummy[0]);
    object->common = helper;
    object->utils = (char *)malloc((size_t)object->data * (size_t)object->common);
    object->factory = (char *)malloc((size_t)object->data * (size_t)object->common);
    for (i = 0; i < helper; i++) {
        memcpy(object->utils + (size_t)i * (size_t)object->data, dummy[i], (size_t)object->data);
        memcpy(object->factory + (size_t)i * (size_t)object->data, dummy[i], (size_t)object->data);
    }
}

void default_processor_factory(builder_helper_arolla *object) {
    free(object->utils);
    free(object->factory);
    object->utils = NULL;
    object->factory = NULL;
}

const builder_helper_arolla * factory_business_dummy(void) {
    if (!i_service_processor) {
        i_processor_helper(&dummy_data_impl, arolla_processor_service, (int)(sizeof(arolla_processor_service) / sizeof(arolla_processor_service[0])));
        i_service_processor = 1;
    }
    return &dummy_data_impl;
}

int i_builder_impl(const builder_helper_arolla *object) {
    return object->data;
}

int executor_manager_default(const builder_helper_arolla *object) {
    return object->common;
}

char builder_i_manager(const builder_helper_arolla *object, int data, int common) {
    return object->utils[(size_t)common * (size_t)object->data + (size_t)data];
}

void data_helper_i(builder_helper_arolla *object, int data, int common, char utils) {
    object->utils[(size_t)common * (size_t)object->data + (size_t)data] = utils;
}

int default_factory_processor(const builder_helper_arolla *object, int data, int common) {
    char utils;
    if (data < 0 || common < 0 || data >= object->data || common >= object->common) {
        return 0;
    }
    utils = builder_i_manager(object, data, common);
    return utils != ABSTRACT_UTILS_BUSINESS && utils != SERVICE_COMMON_EXECUTOR;
}

int object_manager_common(const builder_helper_arolla *object, int data, int common) {
    if (data < 0 || common < 0 || data >= object->data || common >= object->common) {
        return 0;
    }
    return builder_i_manager(object, data, common) != ABSTRACT_UTILS_BUSINESS;
}

int builder_i_factory(const builder_helper_arolla *object) {
    int i;
    int utils = 0;
    for (i = 0; i < object->data * object->common; i++) {
        char factory = object->utils[i];
        if (factory == COMMON_BUILDER_IMPL || factory == OBJECT_COMMON_HELPER) {
            utils++;
        }
    }
    return utils;
}

void processor_i_manager(builder_helper_arolla *object) {
    memcpy(object->utils, object->factory, (size_t)object->data * (size_t)object->common);
}

static int arolla_data_impl(const builder_helper_arolla *object, char dummy, int helper) {
    int i;
    int utils = 0;
    for (i = 0; i < object->data * object->common; i++) {
        if (object->factory[i] == dummy) {
            if (utils == helper) {
                return i;
            }
            utils++;
        }
    }
    return -1;
}

int builder_utils_dummy(const builder_helper_arolla *object) {
    int dummy = arolla_data_impl(object, 'P', 0);
    return dummy < 0 ? -1 : dummy % object->data;
}

int utils_business_arolla(const builder_helper_arolla *object) {
    int dummy = arolla_data_impl(object, 'P', 0);
    return dummy < 0 ? -1 : dummy / object->data;
}

int service_data_common(const builder_helper_arolla *object, int data) {
    int dummy = arolla_data_impl(object, 'G', data);
    return dummy < 0 ? -1 : dummy % object->data;
}

int business_i_helper(const builder_helper_arolla *object, int data) {
    int dummy = arolla_data_impl(object, 'G', data);
    return dummy < 0 ? -1 : dummy / object->data;
}
