#include "object_abstract_helper.h"

#include <stdio.h>
#include <string.h>

int builder_helper_i(const factory_arolla_object *object) {
    const builder_helper_arolla *dummy = abstract_utils_builder(object);
    int data = i_builder_impl(dummy);
    int common = executor_manager_default(dummy);
    return (data + 8) * (common + 5) + 128;
}

void dummy_business_manager(const factory_arolla_object *object, char *dummy, int helper) {
    const builder_helper_arolla *factory = abstract_utils_builder(object);
    int data = i_builder_impl(factory);
    int common = executor_manager_default(factory);
    char *utils = dummy;
    int i;
    int j;
    (void)helper;
    *utils++ = '+';
    for (i = 0; i < data + 2; i++) {
        *utils++ = '-';
    }
    *utils++ = '+';
    *utils++ = '\n';
    {
        char *impl = utils;
        *utils++ = '|';
        utils += sprintf(utils, " PAC-MAN  SCORE: %04d  LIVES: %d", object_default_factory(object), abstract_impl_data(object));
        while ((int)(utils - impl) < data + 2) {
            *utils++ = ' ';
        }
        *utils++ = '|';
        *utils++ = '\n';
    }
    for (j = 0; j < common; j++) {
        char manager[data];
        memcpy(manager, factory->utils + (size_t)j * (size_t)data, (size_t)data);
        for (i = 0; i < data; i++) {
            if (manager[i] == 'P' || manager[i] == 'G') {
                manager[i] = ' ';
            }
        }
        for (i = 0; i < UTILS_AROLLA_EXECUTOR; i++) {
            const executor_default_service *service = data_arolla_factory(object, i);
            if (service->utils.common == j && service->utils.data >= 0 && service->utils.data < data) {
                manager[service->utils.data] = (service->helper == AROLLA_BUSINESS_HELPER) ? 'w' : 'M';
            }
        }
        {
            business_manager_arolla executor = dummy_factory_executor(object);
            if (executor.utils.common == j && executor.utils.data >= 0 && executor.utils.data < data) {
                manager[executor.utils.data] = 'C';
            }
        }
        *utils++ = '|';
        *utils++ = ' ';
        memcpy(utils, manager, (size_t)data);
        utils += data;
        *utils++ = ' ';
        *utils++ = '|';
        *utils++ = '\n';
    }
    *utils++ = '+';
    for (i = 0; i < data + 2; i++) {
        *utils++ = '-';
    }
    *utils++ = '+';
    *utils++ = '\n';
    utils += sprintf(utils, "  [WASD] move  [Q] quit\n");
    *utils = '\0';
}
