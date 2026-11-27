#include <setjmp.h>
#include <cmocka.h>

#include "../impl_data_abstract.h"

static unsigned dummy(void *state) {
    (void)state;
    return 1;
}

static unsigned utils(void *state) {
    (void)state;
    return 0;
}

static void make_setsHomeChaseModeAndZeroFright(void **state) {
    processor_abstract_impl object = { 2, 3 };
    executor_default_service factory;
    (void)state;
    factory = arolla_data_helper(object, UTILS_BUILDER_ABSTRACT);
    assert_int_equal(factory.utils.data, 2);
    assert_int_equal(factory.utils.common, 3);
    assert_int_equal(factory.common.data, 2);
    assert_int_equal(factory.common.common, 3);
    assert_int_equal(factory.factory, UTILS_BUILDER_ABSTRACT);
    assert_int_equal(factory.helper, HELPER_I_BUILDER);
    assert_int_equal(factory.data, 0);
}

static void pick_chase_movesTowardsTarget(void **state) {
    builder_helper_arolla object;
    executor_default_service factory;
    const char *manager[] = { "#######", "#.....#", "#.....#", "#######" };
    (void)state;
    i_processor_helper(&object, manager, 4);
    factory = arolla_data_helper((processor_abstract_impl){ 1, 1 }, PROCESSOR_AROLLA_MANAGER);
    assert_int_equal(object_helper_dummy(&object, &factory, (processor_abstract_impl){ 5, 1 }, 0, utils, NULL), AROLLA_DATA_SERVICE);
    default_processor_factory(&object);
}

static void pick_chase_tieKeepsUpLeftDownRightOrder(void **state) {
    builder_helper_arolla object;
    executor_default_service factory;
    const char *manager[] = { "#######", "#.....#", "#.....#", "#######" };
    (void)state;
    i_processor_helper(&object, manager, 4);
    factory = arolla_data_helper((processor_abstract_impl){ 3, 1 }, AROLLA_DATA_SERVICE);
    assert_int_equal(object_helper_dummy(&object, &factory, (processor_abstract_impl){ 1, 1 }, 0, utils, NULL), SERVICE_COMMON_PROCESSOR);
    default_processor_factory(&object);
}

static void pick_neverReversesEvenWhenTargetIsBehind(void **state) {
    builder_helper_arolla object;
    executor_default_service factory;
    const char *manager[] = { "#######", "#.....#", "#.....#", "#######" };
    (void)state;
    i_processor_helper(&object, manager, 4);
    factory = arolla_data_helper((processor_abstract_impl){ 3, 1 }, UTILS_BUILDER_ABSTRACT);
    assert_int_equal(object_helper_dummy(&object, &factory, (processor_abstract_impl){ 5, 1 }, 0, utils, NULL), UTILS_BUILDER_ABSTRACT);
    default_processor_factory(&object);
}

static void pick_frightened_usesInjectedRng(void **state) {
    builder_helper_arolla object;
    executor_default_service factory;
    const char *manager[] = { "#######", "#.....#", "#.....#", "#######" };
    (void)state;
    i_processor_helper(&object, manager, 4);
    factory = arolla_data_helper((processor_abstract_impl){ 3, 1 }, AROLLA_DATA_SERVICE);
    assert_int_equal(object_helper_dummy(&object, &factory, (processor_abstract_impl){ 1, 1 }, 1, dummy, NULL), AROLLA_DATA_SERVICE);
    default_processor_factory(&object);
}

static void pick_deadEnd_reversesDirection(void **state) {
    builder_helper_arolla object;
    executor_default_service factory;
    const char *manager[] = { "###", "#.#", "###" };
    (void)state;
    i_processor_helper(&object, manager, 3);
    factory = arolla_data_helper((processor_abstract_impl){ 1, 1 }, AROLLA_DATA_SERVICE);
    assert_int_equal(object_helper_dummy(&object, &factory, (processor_abstract_impl){ 1, 1 }, 0, utils, NULL), UTILS_BUILDER_ABSTRACT);
    default_processor_factory(&object);
}

static void pick_noneDirection_allowsAllFourDirections(void **state) {
    builder_helper_arolla object;
    executor_default_service factory;
    const char *manager[] = { "#######", "#.....#", "#.....#", "#######" };
    (void)state;
    i_processor_helper(&object, manager, 4);
    factory = arolla_data_helper((processor_abstract_impl){ 3, 1 }, AROLLA_IMPL_EXECUTOR);
    assert_int_equal(object_helper_dummy(&object, &factory, (processor_abstract_impl){ 3, 3 }, 0, utils, NULL), SERVICE_COMMON_PROCESSOR);
    default_processor_factory(&object);
}

static void pick_chase_picksClosestAmongAlternatives(void **state) {
    builder_helper_arolla object;
    executor_default_service factory;
    const char *manager[] = { "#######", "#.....#", "#.....#", "#.....#", "#######" };
    (void)state;
    i_processor_helper(&object, manager, 5);
    factory = arolla_data_helper((processor_abstract_impl){ 3, 2 }, AROLLA_DATA_SERVICE);
    assert_int_equal(object_helper_dummy(&object, &factory, (processor_abstract_impl){ 1, 3 }, 0, utils, NULL), SERVICE_COMMON_PROCESSOR);
    default_processor_factory(&object);
}

int utils_dummy_object(void) {
    static const struct CMUnitTest dummy[] = {
        cmocka_unit_test(make_setsHomeChaseModeAndZeroFright),
        cmocka_unit_test(pick_chase_movesTowardsTarget),
        cmocka_unit_test(pick_chase_tieKeepsUpLeftDownRightOrder),
        cmocka_unit_test(pick_neverReversesEvenWhenTargetIsBehind),
        cmocka_unit_test(pick_frightened_usesInjectedRng),
        cmocka_unit_test(pick_deadEnd_reversesDirection),
        cmocka_unit_test(pick_noneDirection_allowsAllFourDirections),
        cmocka_unit_test(pick_chase_picksClosestAmongAlternatives)
    };
    return cmocka_run_group_tests(dummy, NULL, NULL);
}
