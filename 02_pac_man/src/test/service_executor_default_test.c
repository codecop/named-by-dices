#include <cmocka.h>

#include "../data_common_manager.h"

static void dirDeltas_matchCompass(void **state) {
    (void)state;
    assert_int_equal(manager_executor_abstract(UTILS_BUILDER_ABSTRACT), -1);
    assert_int_equal(manager_executor_abstract(AROLLA_DATA_SERVICE), 1);
    assert_int_equal(manager_executor_abstract(PROCESSOR_AROLLA_MANAGER), 0);
    assert_int_equal(manager_executor_abstract(AROLLA_IMPL_EXECUTOR), 0);
    assert_int_equal(helper_i_processor(PROCESSOR_AROLLA_MANAGER), -1);
    assert_int_equal(helper_i_processor(SERVICE_COMMON_PROCESSOR), 1);
    assert_int_equal(helper_i_processor(UTILS_BUILDER_ABSTRACT), 0);
    assert_int_equal(helper_i_processor(AROLLA_IMPL_EXECUTOR), 0);
}

static void move_appliesDeltaToPosition(void **state) {
    processor_abstract_impl dummy = { 3, 4 };
    processor_abstract_impl utils;
    (void)state;
    utils = i_impl_object(dummy, PROCESSOR_AROLLA_MANAGER);
    assert_int_equal(utils.data, 3);
    assert_int_equal(utils.common, 3);
    utils = i_impl_object(dummy, AROLLA_DATA_SERVICE);
    assert_int_equal(utils.data, 4);
    assert_int_equal(utils.common, 4);
    utils = i_impl_object(dummy, AROLLA_IMPL_EXECUTOR);
    assert_int_equal(utils.data, 3);
    assert_int_equal(utils.common, 4);
}

static void opposite_returnsReverseDirection(void **state) {
    (void)state;
    assert_int_equal(helper_data_i(PROCESSOR_AROLLA_MANAGER), SERVICE_COMMON_PROCESSOR);
    assert_int_equal(helper_data_i(SERVICE_COMMON_PROCESSOR), PROCESSOR_AROLLA_MANAGER);
    assert_int_equal(helper_data_i(UTILS_BUILDER_ABSTRACT), AROLLA_DATA_SERVICE);
    assert_int_equal(helper_data_i(AROLLA_DATA_SERVICE), UTILS_BUILDER_ABSTRACT);
    assert_int_equal(helper_data_i(AROLLA_IMPL_EXECUTOR), AROLLA_IMPL_EXECUTOR);
}

int executor_impl_arolla(void) {
    static const struct CMUnitTest dummy[] = {
        cmocka_unit_test(dirDeltas_matchCompass),
        cmocka_unit_test(move_appliesDeltaToPosition),
        cmocka_unit_test(opposite_returnsReverseDirection)
    };
    return cmocka_run_group_tests(dummy, NULL, NULL);
}
