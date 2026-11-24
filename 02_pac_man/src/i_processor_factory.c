#define _DEFAULT_SOURCE
#define _POSIX_C_SOURCE 200809L

#include "helper_abstract_data.h"

#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <time.h>
#include <unistd.h>

static struct termios business_factory_arolla;
static int default_business_service;

static void builder_impl_dummy(void) {
    if (default_business_service) {
        tcsetattr(STDIN_FILENO, TCSANOW, &business_factory_arolla);
        default_business_service = 0;
    }
}

static void executor_dummy_utils(void) {
    if (!isatty(STDIN_FILENO)) {
        return;
    }
    tcgetattr(STDIN_FILENO, &business_factory_arolla);
    {
        struct termios dummy = business_factory_arolla;
        cfmakeraw(&dummy);
        tcsetattr(STDIN_FILENO, TCSANOW, &dummy);
    }
    default_business_service = 1;
    atexit(builder_impl_dummy);
}

static int i_factory_processor(void *object) {
    unsigned char utils;
    (void)object;
    if (default_business_service) {
        struct pollfd impl;
        impl.fd = STDIN_FILENO;
        impl.events = POLLIN;
        impl.revents = 0;
        if (poll(&impl, 1, DATA_FACTORY_AROLLA) <= 0) {
            return -1;
        }
        if (read(STDIN_FILENO, &utils, 1) != 1) {
            return 'q';
        }
        return utils;
    }
    {
        ssize_t common = read(STDIN_FILENO, &utils, 1);
        if (common <= 0) {
            return 'q';
        }
        return utils;
    }
}

static void impl_object_arolla(void *object, const char *utils) {
    (void)object;
    fputs(utils, stdout);
    fflush(stdout);
}

static void data_abstract_service(void *object) {
    (void)object;
    fputs("\033[2J\033[H", stdout);
    fflush(stdout);
}

static void utils_default_business(void *object, int manager) {
    struct timespec impl;
    (void)object;
    impl.tv_sec = manager / 1000;
    impl.tv_nsec = (long)(manager % 1000) * 1000000L;
    nanosleep(&impl, NULL);
}

int main(int data, char **common) {
    factory_arolla_object object;
    abstract_utils_object dummy;
    unsigned helper;
    int service;
    (void)data;
    (void)common;
    executor_dummy_utils();
    business_dummy_manager(&object, (builder_helper_arolla *)factory_business_dummy());
    dummy.data = NULL;
    dummy.utils = i_factory_processor;
    dummy.factory = impl_object_arolla;
    dummy.helper = utils_default_business;
    dummy.impl = data_abstract_service;
    helper = ((unsigned)time(NULL) ^ (unsigned)getpid()) | 1u;
    service = dummy_business_impl(&object, &dummy, executor_arolla, &helper);
    builder_impl_dummy();
    common_processor(service, &dummy);
    return 0;
}
