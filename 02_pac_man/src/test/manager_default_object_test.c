#include <stdlib.h>
#include <string.h>
#include <setjmp.h>
#include <cmocka.h>

#include "../object_abstract_helper.h"

static int dummy(const char *object, int factory) {
    int utils = 0;
    while (*object) {
        if (*object == (char)factory) {
            utils++;
        }
        object++;
    }
    return utils;
}

static void frame_startsWithBorderAndContainsHud(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    char *manager;
    const char *service[] = { "#####", "#P.G#", "#...#", "#####" };
    (void)state;
    i_processor_helper(&object, service, 4);
    business_dummy_manager(&factory, &object);
    manager = (char *)malloc((size_t)builder_helper_i(&factory));
    dummy_business_manager(&factory, manager, builder_helper_i(&factory));
    assert_int_equal(manager[0], '+');
    assert_non_null(strstr(manager, "PAC-MAN"));
    assert_non_null(strstr(manager, "SCORE: 0000"));
    assert_non_null(strstr(manager, "LIVES:"));
    assert_non_null(strstr(manager, "[WASD] move  [Q] quit"));
    free(manager);
    default_processor_factory(&object);
}

static void frame_drawsWallsDotsAndActors(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    char *manager;
    const char *service[] = { "#####", "#P.G#", "#...#", "#####" };
    (void)state;
    i_processor_helper(&object, service, 4);
    business_dummy_manager(&factory, &object);
    manager = (char *)malloc((size_t)builder_helper_i(&factory));
    dummy_business_manager(&factory, manager, builder_helper_i(&factory));
    assert_non_null(strstr(manager, "#####"));
    assert_int_equal(dummy(manager, '#'), 14);
    assert_int_equal(dummy(manager, '.'), 4);
    assert_non_null(strstr(manager, "#C.M#"));
    free(manager);
    default_processor_factory(&object);
}

static void frame_fitsIntoFrameSizeBuffer(void **state) {
    factory_arolla_object factory;
    char *manager;
    int utils;
    (void)state;
    business_dummy_manager(&factory, (builder_helper_arolla *)factory_business_dummy());
    utils = builder_helper_i(&factory);
    manager = (char *)malloc((size_t)utils);
    dummy_business_manager(&factory, manager, utils);
    assert_true((int)strlen(manager) < utils);
    free(manager);
}

static void frame_frightenedGhost_isDrawnAsLowercaseW(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    char *manager;
    const char *service[] = { "#####", "#P.G#", "#...#", "#####" };
    (void)state;
    i_processor_helper(&object, service, 4);
    business_dummy_manager(&factory, &object);
    factory.factory[0].helper = AROLLA_BUSINESS_HELPER;
    factory.factory[0].data = 9;
    manager = (char *)malloc((size_t)builder_helper_i(&factory));
    dummy_business_manager(&factory, manager, builder_helper_i(&factory));
    assert_int_equal(dummy(manager, 'w'), 1);
    assert_non_null(strstr(manager, "#C.w#"));
    free(manager);
    default_processor_factory(&object);
}

static void frame_wideMap_padsHudLineToBorder(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    char *manager;
    char *utils;
    const char *service[] = { "########################################", "#P....................................G#", "########################################" };
    (void)state;
    i_processor_helper(&object, service, 3);
    business_dummy_manager(&factory, &object);
    manager = (char *)malloc((size_t)builder_helper_i(&factory));
    dummy_business_manager(&factory, manager, builder_helper_i(&factory));
    utils = strstr(manager, "PAC-MAN");
    assert_non_null(utils);
    assert_int_equal((int)(strchr(utils, '\n') - utils), 41);
    free(manager);
    default_processor_factory(&object);
}

static void frame_outOfBoundsActors_areSkipped(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    char *manager;
    const char *service[] = { "#####", "#P.G#", "#####" };
    (void)state;
    i_processor_helper(&object, service, 3);
    business_dummy_manager(&factory, &object);
    manager = (char *)malloc((size_t)builder_helper_i(&factory));
    factory.factory[0].utils.data = 999;
    factory.utils.utils.data = -1;
    dummy_business_manager(&factory, manager, builder_helper_i(&factory));
    assert_non_null(strstr(manager, "# . #"));
    assert_int_equal(dummy(manager, 'M'), 1);
    assert_int_equal(dummy(manager, 'C'), 2);
    factory.factory[0].utils.data = -1;
    factory.utils.utils.data = 999;
    dummy_business_manager(&factory, manager, builder_helper_i(&factory));
    assert_non_null(strstr(manager, "# . #"));
    assert_int_equal(dummy(manager, 'M'), 1);
    assert_int_equal(dummy(manager, 'C'), 2);
    free(manager);
    default_processor_factory(&object);
}

int business_manager_default(void) {
    static const struct CMUnitTest dummy[] = {
        cmocka_unit_test(frame_startsWithBorderAndContainsHud),
        cmocka_unit_test(frame_drawsWallsDotsAndActors),
        cmocka_unit_test(frame_fitsIntoFrameSizeBuffer),
        cmocka_unit_test(frame_frightenedGhost_isDrawnAsLowercaseW),
        cmocka_unit_test(frame_wideMap_padsHudLineToBorder),
        cmocka_unit_test(frame_outOfBoundsActors_areSkipped)
    };
    return cmocka_run_group_tests(dummy, NULL, NULL);
}
