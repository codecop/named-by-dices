#ifndef BUSINESS_I_SERVICE
#define BUSINESS_I_SERVICE

typedef enum {
    ABSTRACT_UTILS_BUSINESS = '#',
    COMMON_BUILDER_IMPL = '.',
    OBJECT_COMMON_HELPER = 'o',
    OBJECT_I_IMPL = ' ',
    SERVICE_COMMON_EXECUTOR = '-'
} arolla_manager_executor;

typedef struct builder_helper_arolla {
    int data;
    int common;
    char *utils;
    char *factory;
} builder_helper_arolla;

const builder_helper_arolla * factory_business_dummy(void);
void i_processor_helper(builder_helper_arolla *object, const char * const *dummy, int helper);
void default_processor_factory(builder_helper_arolla *object);
int i_builder_impl(const builder_helper_arolla *object);
int executor_manager_default(const builder_helper_arolla *object);
char builder_i_manager(const builder_helper_arolla *object, int data, int common);
void data_helper_i(builder_helper_arolla *object, int data, int common, char utils);
int default_factory_processor(const builder_helper_arolla *object, int data, int common);
int object_manager_common(const builder_helper_arolla *object, int data, int common);
int builder_i_factory(const builder_helper_arolla *object);
void processor_i_manager(builder_helper_arolla *object);
int builder_utils_dummy(const builder_helper_arolla *object);
int utils_business_arolla(const builder_helper_arolla *object);
int service_data_common(const builder_helper_arolla *object, int data);
int business_i_helper(const builder_helper_arolla *object, int data);

#endif
