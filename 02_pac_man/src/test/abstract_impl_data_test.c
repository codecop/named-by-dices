#include <stddef.h>
#include <string.h>
#include <setjmp.h>
#include <cmocka.h>

#include "../helper_abstract_data.h"

static int arolla[64];
static int builder;
static int business;
static char common[16384];
static int data;
static int executor;
static int factory;
static int helper;

static int dummy(void *object) {
    (void)object;
    if (business >= builder) {
        return -1;
    }
    return arolla[business++];
}

static void utils(void *object, const char *dummy) {
    size_t manager = strlen(dummy);
    (void)object;
    if (data + (int)manager < (int)sizeof(common)) {
        memcpy(common + data, dummy, manager);
        data += (int)manager;
        common[data] = '\0';
    }
    executor++;
}

static void service(void *object, int dummy) {
    (void)object;
    (void)dummy;
    helper++;
}

static void impl(void *object) {
    (void)object;
    factory++;
}

static unsigned manager(void *object) {
    (void)object;
    return 0;
}

static void processor(void) {
    builder = 0;
    business = 0;
    data = 0;
    executor = 0;
    factory = 0;
    helper = 0;
    common[0] = '\0';
}

static void keyDir_mapsWasdToDirectionsAndRestToNone(void **state) {
    (void)state;
    assert_int_equal(executor_common_helper('w'), PROCESSOR_AROLLA_MANAGER);
    assert_int_equal(executor_common_helper('a'), UTILS_BUILDER_ABSTRACT);
    assert_int_equal(executor_common_helper('s'), SERVICE_COMMON_PROCESSOR);
    assert_int_equal(executor_common_helper('d'), AROLLA_DATA_SERVICE);
    assert_int_equal(executor_common_helper('x'), AROLLA_IMPL_EXECUTOR);
    assert_int_equal(executor_common_helper(-1), AROLLA_IMPL_EXECUTOR);
}

static void run_quitsWhenQPressed_rendersTwiceAndStaysRunning(void **state) {
    builder_helper_arolla object_common_impl;
    factory_arolla_object builder_common_factory;
    abstract_utils_object business_common_utils;
    const char *data_common_helper[] = { "#######", "#P....#", "#..G..#", "#######" };
    (void)state;
    processor();
    arolla[0] = 'q';
    builder = 1;
    i_processor_helper(&object_common_impl, data_common_helper, 4);
    business_dummy_manager(&builder_common_factory, &object_common_impl);
    business_common_utils.data = NULL;
    business_common_utils.utils = dummy;
    business_common_utils.factory = utils;
    business_common_utils.helper = service;
    business_common_utils.impl = impl;
    assert_int_equal(dummy_business_impl(&builder_common_factory, &business_common_utils, manager, NULL), BUSINESS_SERVICE_I);
    assert_int_equal(factory, 2);
    assert_int_equal(executor, 2);
    assert_int_equal(helper, 1);
    assert_non_null(strstr(common, "SCORE"));
    default_processor_factory(&object_common_impl);
}

static void run_dKeySteersPacRightAndEatsDot(void **state) {
    builder_helper_arolla object_common_impl;
    factory_arolla_object builder_common_factory;
    abstract_utils_object business_common_utils;
    const char *data_common_helper[] = { "#######", "#P....#", "#..G..#", "#######" };
    (void)state;
    processor();
    arolla[0] = 'd';
    arolla[1] = 'q';
    builder = 2;
    i_processor_helper(&object_common_impl, data_common_helper, 4);
    business_dummy_manager(&builder_common_factory, &object_common_impl);
    business_common_utils.data = NULL;
    business_common_utils.utils = dummy;
    business_common_utils.factory = utils;
    business_common_utils.helper = service;
    business_common_utils.impl = impl;
    assert_int_equal(dummy_business_impl(&builder_common_factory, &business_common_utils, manager, NULL), BUSINESS_SERVICE_I);
    assert_int_equal(dummy_factory_executor(&builder_common_factory).utils.data, 2);
    assert_int_equal(object_default_factory(&builder_common_factory), FACTORY_OBJECT_ABSTRACT);
    default_processor_factory(&object_common_impl);
}

static void run_exitsWithWonWhenLastDotIsEaten(void **state) {
    builder_helper_arolla object_common_impl;
    factory_arolla_object builder_common_factory;
    abstract_utils_object business_common_utils;
    const char *data_common_helper[] = { "#####", "#P..#", "#####" };
    (void)state;
    processor();
    arolla[0] = 'd';
    builder = 1;
    i_processor_helper(&object_common_impl, data_common_helper, 3);
    business_dummy_manager(&builder_common_factory, &object_common_impl);
    builder_common_factory.impl = 1;
    business_common_utils.data = NULL;
    business_common_utils.utils = dummy;
    business_common_utils.factory = utils;
    business_common_utils.helper = service;
    business_common_utils.impl = impl;
    assert_int_equal(dummy_business_impl(&builder_common_factory, &business_common_utils, manager, NULL), AROLLA_IMPL_BUSINESS);
    default_processor_factory(&object_common_impl);
}

static void run_exitsWithLostWhenGhostsCatchPacUntilNoLives(void **state) {
    builder_helper_arolla object_common_impl;
    factory_arolla_object builder_common_factory;
    abstract_utils_object business_common_utils;
    const char *data_common_helper[] = { "#####", "#PG.#", "#####" };
    (void)state;
    processor();
    i_processor_helper(&object_common_impl, data_common_helper, 3);
    business_dummy_manager(&builder_common_factory, &object_common_impl);
    business_common_utils.data = NULL;
    business_common_utils.utils = dummy;
    business_common_utils.factory = utils;
    business_common_utils.helper = service;
    business_common_utils.impl = impl;
    assert_int_equal(dummy_business_impl(&builder_common_factory, &business_common_utils, manager, NULL), EXECUTOR_DUMMY_IMPL);
    assert_int_equal(abstract_impl_data(&builder_common_factory), 0);
    default_processor_factory(&object_common_impl);
}

static void announce_won_writesYouWin(void **state) {
    abstract_utils_object business_common_utils;
    (void)state;
    processor();
    business_common_utils.data = NULL;
    business_common_utils.factory = utils;
    common_processor((int)AROLLA_IMPL_BUSINESS, &business_common_utils);
    assert_non_null(strstr(common, "YOU WIN!"));
}

static void announce_lost_writesGameOver(void **state) {
    abstract_utils_object business_common_utils;
    (void)state;
    processor();
    business_common_utils.data = NULL;
    business_common_utils.factory = utils;
    common_processor((int)EXECUTOR_DUMMY_IMPL, &business_common_utils);
    assert_non_null(strstr(common, "GAME OVER"));
}

static void announce_running_writesBye(void **state) {
    abstract_utils_object business_common_utils;
    (void)state;
    processor();
    business_common_utils.data = NULL;
    business_common_utils.factory = utils;
    common_processor((int)BUSINESS_SERVICE_I, &business_common_utils);
    assert_non_null(strstr(common, "BYE"));
}

static void xorshift_isDeterministicAndAdvancesState(void **state) {
    unsigned object_common_impl = 12345u;
    unsigned builder_common_factory = 12345u;
    unsigned utils_dummy;
    unsigned impl_dummy;
    (void)state;
    utils_dummy = executor_arolla(&object_common_impl);
    impl_dummy = executor_arolla(&builder_common_factory);
    assert_int_equal(utils_dummy, impl_dummy);
    assert_true(object_common_impl != 12345u);
    assert_true(utils_dummy != 0u);
}

int arolla_processor_utils(void) {
    static const struct CMUnitTest dummy[] = {
        cmocka_unit_test(keyDir_mapsWasdToDirectionsAndRestToNone),
        cmocka_unit_test(run_quitsWhenQPressed_rendersTwiceAndStaysRunning),
        cmocka_unit_test(run_dKeySteersPacRightAndEatsDot),
        cmocka_unit_test(run_exitsWithWonWhenLastDotIsEaten),
        cmocka_unit_test(run_exitsWithLostWhenGhostsCatchPacUntilNoLives),
        cmocka_unit_test(announce_won_writesYouWin),
        cmocka_unit_test(announce_lost_writesGameOver),
        cmocka_unit_test(announce_running_writesBye),
        cmocka_unit_test(xorshift_isDeterministicAndAdvancesState)
    };
    return cmocka_run_group_tests(dummy, NULL, NULL);
}
