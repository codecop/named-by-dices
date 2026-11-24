#include <cmocka.h>

#include "../data_utils_arolla.h"

static unsigned dummy(void *state) {
    (void)state;
    return 0;
}

static void newGame_initialisesStateFromMap(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    const char *manager[] = { "#####", "#P..#", "#.G.#", "#####" };
    (void)state;
    i_processor_helper(&object, manager, 4);
    business_dummy_manager(&factory, &object);
    assert_int_equal(abstract_executor_impl(&factory), BUSINESS_SERVICE_I);
    assert_int_equal(object_default_factory(&factory), 0);
    assert_int_equal(abstract_impl_data(&factory), IMPL_I_PROCESSOR);
    assert_int_equal(default_processor_utils(&factory), 4);
    assert_int_equal(dummy_factory_executor(&factory).utils.data, 1);
    assert_int_equal(dummy_factory_executor(&factory).utils.common, 1);
    assert_int_equal(data_arolla_factory(&factory, 0)->utils.data, 2);
    assert_int_equal(data_arolla_factory(&factory, 0)->utils.common, 2);
    default_processor_factory(&object);
}

static void step_openWish_movesPacAndEatsDot(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    const char *manager[] = { "#####", "#P..#", "#####" };
    (void)state;
    i_processor_helper(&object, manager, 3);
    business_dummy_manager(&factory, &object);
    i_utils_builder(&factory, AROLLA_DATA_SERVICE, dummy, NULL);
    assert_int_equal(dummy_factory_executor(&factory).utils.data, 2);
    assert_int_equal(dummy_factory_executor(&factory).utils.common, 1);
    assert_int_equal(object_default_factory(&factory), FACTORY_OBJECT_ABSTRACT);
    assert_int_equal(default_processor_utils(&factory), 1);
    default_processor_factory(&object);
}

static void step_blockedWishAndDir_keepsPacInPlace(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    const char *manager[] = { "#####", "#P..#", "#####" };
    (void)state;
    i_processor_helper(&object, manager, 3);
    business_dummy_manager(&factory, &object);
    i_utils_builder(&factory, PROCESSOR_AROLLA_MANAGER, dummy, NULL);
    assert_int_equal(dummy_factory_executor(&factory).utils.data, 1);
    assert_int_equal(dummy_factory_executor(&factory).utils.common, 1);
    assert_int_equal(object_default_factory(&factory), 0);
    assert_int_equal(default_processor_utils(&factory), 2);
    default_processor_factory(&object);
}

static void step_pellet_frightensGhostsAndScores50(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    const char *manager[] = { "#####", "#Po.#", "#####" };
    (void)state;
    i_processor_helper(&object, manager, 3);
    business_dummy_manager(&factory, &object);
    i_utils_builder(&factory, AROLLA_DATA_SERVICE, dummy, NULL);
    assert_int_equal(object_default_factory(&factory), BUILDER_AROLLA_SERVICE);
    assert_int_equal(data_arolla_factory(&factory, 0)->helper, AROLLA_BUSINESS_HELPER);
    assert_int_equal(data_arolla_factory(&factory, 0)->data, OBJECT_COMMON_MANAGER);
    default_processor_factory(&object);
}

static void step_frightenedGhostTouch_eatsGhostFor200AndRespawns(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    const char *manager[] = { "####", "#PG#", "#.##" };
    (void)state;
    i_processor_helper(&object, manager, 3);
    business_dummy_manager(&factory, &object);
    factory.factory[0].helper = AROLLA_BUSINESS_HELPER;
    factory.factory[0].data = 5;
    i_utils_builder(&factory, AROLLA_IMPL_EXECUTOR, dummy, NULL);
    i_utils_builder(&factory, AROLLA_IMPL_EXECUTOR, dummy, NULL);
    assert_int_equal(object_default_factory(&factory), UTILS_AROLLA_PROCESSOR);
    assert_int_equal(data_arolla_factory(&factory, 0)->utils.data, 2);
    assert_int_equal(data_arolla_factory(&factory, 0)->utils.common, 1);
    assert_int_equal(data_arolla_factory(&factory, 0)->helper, HELPER_I_BUILDER);
    assert_int_equal(abstract_executor_impl(&factory), BUSINESS_SERVICE_I);
    assert_int_equal(abstract_impl_data(&factory), IMPL_I_PROCESSOR);
    default_processor_factory(&object);
}

static void step_chasingGhostTouch_costsLifeAndResetsActors(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    const char *manager[] = { "####", "#PG#", "#.##" };
    (void)state;
    i_processor_helper(&object, manager, 3);
    business_dummy_manager(&factory, &object);
    i_utils_builder(&factory, AROLLA_IMPL_EXECUTOR, dummy, NULL);
    i_utils_builder(&factory, AROLLA_IMPL_EXECUTOR, dummy, NULL);
    assert_int_equal(abstract_impl_data(&factory), IMPL_I_PROCESSOR - 1);
    assert_int_equal(dummy_factory_executor(&factory).utils.data, 1);
    assert_int_equal(dummy_factory_executor(&factory).utils.common, 1);
    assert_int_equal(data_arolla_factory(&factory, 0)->utils.data, 2);
    assert_int_equal(abstract_executor_impl(&factory), BUSINESS_SERVICE_I);
    default_processor_factory(&object);
}

static void step_lastLifeLost_setsStatusLost(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    const char *manager[] = { "####", "#PG#", "#.##" };
    (void)state;
    i_processor_helper(&object, manager, 3);
    business_dummy_manager(&factory, &object);
    factory.helper = 1;
    i_utils_builder(&factory, AROLLA_IMPL_EXECUTOR, dummy, NULL);
    i_utils_builder(&factory, AROLLA_IMPL_EXECUTOR, dummy, NULL);
    assert_int_equal(abstract_executor_impl(&factory), EXECUTOR_DUMMY_IMPL);
    assert_int_equal(abstract_impl_data(&factory), 0);
    default_processor_factory(&object);
}

static void step_allDotsEaten_setsStatusWon(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    const char *manager[] = { "#####", "#P..#", "#####" };
    (void)state;
    i_processor_helper(&object, manager, 3);
    business_dummy_manager(&factory, &object);
    factory.impl = 1;
    i_utils_builder(&factory, AROLLA_DATA_SERVICE, dummy, NULL);
    assert_int_equal(abstract_executor_impl(&factory), AROLLA_IMPL_BUSINESS);
    assert_int_equal(object_default_factory(&factory), FACTORY_OBJECT_ABSTRACT);
    default_processor_factory(&object);
}

static void step_whenNotRunning_changesNothing(void **state) {
    builder_helper_arolla object;
    factory_arolla_object factory;
    const char *manager[] = { "####", "#PG#", "#.##" };
    int utils;
    (void)state;
    i_processor_helper(&object, manager, 3);
    business_dummy_manager(&factory, &object);
    factory.helper = 1;
    i_utils_builder(&factory, AROLLA_IMPL_EXECUTOR, dummy, NULL);
    i_utils_builder(&factory, AROLLA_IMPL_EXECUTOR, dummy, NULL);
    assert_int_equal(abstract_executor_impl(&factory), EXECUTOR_DUMMY_IMPL);
    utils = object_default_factory(&factory);
    i_utils_builder(&factory, AROLLA_DATA_SERVICE, dummy, NULL);
    assert_int_equal(object_default_factory(&factory), utils);
    assert_int_equal(abstract_executor_impl(&factory), EXECUTOR_DUMMY_IMPL);
    default_processor_factory(&object);
}

int data_helper_common(void) {
    static const struct CMUnitTest dummy[] = {
        cmocka_unit_test(newGame_initialisesStateFromMap),
        cmocka_unit_test(step_openWish_movesPacAndEatsDot),
        cmocka_unit_test(step_blockedWishAndDir_keepsPacInPlace),
        cmocka_unit_test(step_pellet_frightensGhostsAndScores50),
        cmocka_unit_test(step_frightenedGhostTouch_eatsGhostFor200AndRespawns),
        cmocka_unit_test(step_chasingGhostTouch_costsLifeAndResetsActors),
        cmocka_unit_test(step_lastLifeLost_setsStatusLost),
        cmocka_unit_test(step_allDotsEaten_setsStatusWon),
        cmocka_unit_test(step_whenNotRunning_changesNothing)
    };
    return cmocka_run_group_tests(dummy, NULL, NULL);
}
