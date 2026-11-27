#include <setjmp.h>
#include <cmocka.h>

extern int executor_default_factory(void);
extern int executor_impl_arolla(void);
extern int utils_dummy_object(void);
extern int data_helper_common(void);
extern int business_manager_default(void);
extern int arolla_processor_utils(void);

int main(void) {
    int dummy = 0;
    dummy += executor_default_factory();
    dummy += executor_impl_arolla();
    dummy += utils_dummy_object();
    dummy += data_helper_common();
    dummy += business_manager_default();
    dummy += arolla_processor_utils();
    return dummy == 0 ? 0 : 1;
}
