#include <stddef.h>
#include <cmocka.h>

#include "../business_i_service.h"

static void defaultBoard_has21ColumnsAnd15Rows(void **state) {
    const builder_helper_arolla *dummy;
    (void)state;
    dummy = factory_business_dummy();
    assert_int_equal(i_builder_impl(dummy), 21);
    assert_int_equal(executor_manager_default(dummy), 15);
}

static void defaultBoard_borderIsAllWalls(void **state) {
    const builder_helper_arolla *dummy;
    int i;
    (void)state;
    dummy = factory_business_dummy();
    for (i = 0; i < i_builder_impl(dummy); i++) {
        assert_int_equal(builder_i_manager(dummy, i, 0), ABSTRACT_UTILS_BUSINESS);
        assert_int_equal(builder_i_manager(dummy, i, executor_manager_default(dummy) - 1), ABSTRACT_UTILS_BUSINESS);
    }
    for (i = 0; i < executor_manager_default(dummy); i++) {
        assert_int_equal(builder_i_manager(dummy, 0, i), ABSTRACT_UTILS_BUSINESS);
        assert_int_equal(builder_i_manager(dummy, i_builder_impl(dummy) - 1, i), ABSTRACT_UTILS_BUSINESS);
    }
}

static void defaultBoard_counts161Edibles(void **state) {
    (void)state;
    assert_int_equal(builder_i_factory(factory_business_dummy()), 161);
}

static void defaultBoard_pacStartIsAt10x11(void **state) {
    const builder_helper_arolla *dummy;
    (void)state;
    dummy = factory_business_dummy();
    assert_int_equal(builder_utils_dummy(dummy), 10);
    assert_int_equal(utils_business_arolla(dummy), 11);
}

static void defaultBoard_ghostStartsAreInHouse(void **state) {
    const builder_helper_arolla *dummy;
    (void)state;
    dummy = factory_business_dummy();
    assert_int_equal(service_data_common(dummy, 0), 9);
    assert_int_equal(business_i_helper(dummy, 0), 8);
    assert_int_equal(service_data_common(dummy, 1), 10);
    assert_int_equal(business_i_helper(dummy, 1), 8);
    assert_int_equal(service_data_common(dummy, 2), 11);
    assert_int_equal(business_i_helper(dummy, 2), 8);
}

static void door_blocksPacButNotGhost_wallBlocksBoth_dotPassesBoth(void **state) {
    const builder_helper_arolla *dummy;
    (void)state;
    dummy = factory_business_dummy();
    assert_int_equal(default_factory_processor(dummy, 10, 7), 0);
    assert_int_equal(object_manager_common(dummy, 10, 7), 1);
    assert_int_equal(default_factory_processor(dummy, 0, 0), 0);
    assert_int_equal(object_manager_common(dummy, 0, 0), 0);
    assert_int_equal(default_factory_processor(dummy, 1, 1), 1);
    assert_int_equal(object_manager_common(dummy, 1, 1), 1);
}

static void outOfBounds_isNotPassable(void **state) {
    const builder_helper_arolla *dummy;
    (void)state;
    dummy = factory_business_dummy();
    assert_int_equal(default_factory_processor(dummy, -1, 0), 0);
    assert_int_equal(object_manager_common(dummy, -1, 0), 0);
    assert_int_equal(default_factory_processor(dummy, 21, 0), 0);
    assert_int_equal(object_manager_common(dummy, 0, 15), 0);
}

static void customBoard_setCellThenReset_restoresMap(void **state) {
    builder_helper_arolla dummy;
    const char *factory[] = { "#####", "#P.G#", "#####" };
    (void)state;
    i_processor_helper(&dummy, factory, 3);
    assert_int_equal(i_builder_impl(&dummy), 5);
    assert_int_equal(executor_manager_default(&dummy), 3);
    assert_int_equal(builder_i_manager(&dummy, 1, 1), 'P');
    assert_int_equal(builder_utils_dummy(&dummy), 1);
    assert_int_equal(utils_business_arolla(&dummy), 1);
    assert_int_equal(service_data_common(&dummy, 0), 3);
    assert_int_equal(business_i_helper(&dummy, 0), 1);
    assert_int_equal(builder_i_factory(&dummy), 1);
    data_helper_i(&dummy, 1, 1, COMMON_BUILDER_IMPL);
    assert_int_equal(builder_i_manager(&dummy, 1, 1), COMMON_BUILDER_IMPL);
    assert_int_equal(builder_i_factory(&dummy), 2);
    processor_i_manager(&dummy);
    assert_int_equal(builder_i_manager(&dummy, 1, 1), 'P');
    default_processor_factory(&dummy);
}

int executor_default_factory(void) {
    static const struct CMUnitTest dummy[] = {
        cmocka_unit_test(defaultBoard_has21ColumnsAnd15Rows),
        cmocka_unit_test(defaultBoard_borderIsAllWalls),
        cmocka_unit_test(defaultBoard_counts161Edibles),
        cmocka_unit_test(defaultBoard_pacStartIsAt10x11),
        cmocka_unit_test(defaultBoard_ghostStartsAreInHouse),
        cmocka_unit_test(door_blocksPacButNotGhost_wallBlocksBoth_dotPassesBoth),
        cmocka_unit_test(outOfBounds_isNotPassable),
        cmocka_unit_test(customBoard_setCellThenReset_restoresMap)
    };
    return cmocka_run_group_tests(dummy, NULL, NULL);
}
