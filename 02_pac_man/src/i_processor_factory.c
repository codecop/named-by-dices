#ifndef _WIN32
#define _DEFAULT_SOURCE
#define _POSIX_C_SOURCE 200809L
#endif

#include "helper_abstract_data.h"

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef _WIN32
#include <conio.h>
#include <io.h>
#include <windows.h>
#else
#include <poll.h>
#include <termios.h>
#include <unistd.h>
#endif

#ifdef _WIN32
static DWORD business_factory_arolla;
static DWORD executor_common_factory;
static int arolla_service_utils;
static int object_utils_impl;
#else
static struct termios business_factory_arolla;
#endif
static int default_business_service;

static void builder_impl_dummy(void) {
#ifdef _WIN32
    if (object_utils_impl) {
        SetConsoleMode(GetStdHandle(STD_OUTPUT_HANDLE), executor_common_factory);
        object_utils_impl = 0;
    }
#endif
    if (default_business_service) {
#ifdef _WIN32
        SetConsoleMode(GetStdHandle(STD_INPUT_HANDLE), business_factory_arolla);
#else
        tcsetattr(STDIN_FILENO, TCSANOW, &business_factory_arolla);
#endif
        default_business_service = 0;
    }
}

static void executor_dummy_utils(void) {
#ifdef _WIN32
    HANDLE dummy;
    DWORD manager;
    dummy = GetStdHandle(STD_OUTPUT_HANDLE);
    if (GetConsoleMode(dummy, &manager)) {
        executor_common_factory = manager;
        object_utils_impl = 1;
        arolla_service_utils = SetConsoleMode(dummy, manager | ENABLE_VIRTUAL_TERMINAL_PROCESSING) ? 1 : 0;
    }
    if (!_isatty(_fileno(stdin))) {
        return;
    }
    dummy = GetStdHandle(STD_INPUT_HANDLE);
    if (GetConsoleMode(dummy, &manager)) {
        business_factory_arolla = manager;
        if (SetConsoleMode(dummy, (manager & ~(DWORD)(ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT)) | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
            || SetConsoleMode(dummy, manager & ~(DWORD)(ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT))) {
            default_business_service = 1;
            atexit(builder_impl_dummy);
        }
    }
#else
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
#endif
}

static int i_factory_processor(void *object) {
    (void)object;
#ifdef _WIN32
    if (default_business_service) {
        int manager = DATA_FACTORY_AROLLA;
        while (manager > 0) {
            if (_kbhit()) {
                return _getch();
            }
            Sleep(10);
            manager -= 10;
        }
        return -1;
    }
    {
        int common = getchar();
        if (common == EOF) {
            return 'q';
        }
        return common;
    }
#else
    {
        unsigned char utils;
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
#endif
}

static void impl_object_arolla(void *object, const char *utils) {
    (void)object;
    fputs(utils, stdout);
    fflush(stdout);
}

static void data_abstract_service(void *object) {
    (void)object;
#ifdef _WIN32
    if (arolla_service_utils) {
        fputs("\033[2J\033[H", stdout);
        fflush(stdout);
    } else {
        system("cls");
    }
#else
    fputs("\033[2J\033[H", stdout);
    fflush(stdout);
#endif
}

static void utils_default_business(void *object, int manager) {
    (void)object;
#ifdef _WIN32
    Sleep((DWORD)manager);
#else
    {
        struct timespec impl;
        impl.tv_sec = manager / 1000;
        impl.tv_nsec = (long)(manager % 1000) * 1000000L;
        nanosleep(&impl, NULL);
    }
#endif
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
#ifdef _WIN32
    helper = (GetTickCount() ^ (unsigned)GetCurrentProcessId()) | 1u;
#else
    helper = ((unsigned)time(NULL) ^ (unsigned)getpid()) | 1u;
#endif
    service = dummy_business_impl(&object, &dummy, executor_arolla, &helper);
    builder_impl_dummy();
    common_processor(service, &dummy);
    return 0;
}
