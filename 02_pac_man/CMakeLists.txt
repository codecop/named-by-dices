cmake_minimum_required(VERSION 3.16)
project(pac_man C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

if(MSVC)
    add_compile_options(/W4 /WX)
else()
    add_compile_options(-Wall -Wextra -Werror -pedantic)
endif()

set(CMOCKA_ROOT "" CACHE PATH "cmocka installation prefix (x86 or x64 build) containing include/ and lib/")

file(GLOB LIB_SRC CONFIGURE_DEPENDS src/*.c)
list(REMOVE_ITEM LIB_SRC "${CMAKE_CURRENT_SOURCE_DIR}/src/i_processor_factory.c")

add_executable(pacman ${LIB_SRC} src/i_processor_factory.c)

file(GLOB TEST_SRC CONFIGURE_DEPENDS src/test/*_test.c)
add_executable(run_tests ${LIB_SRC} ${TEST_SRC})
target_include_directories(run_tests PRIVATE src)

find_path(CMOCKA_INCLUDE_DIR NAMES cmocka.h HINTS "${CMOCKA_ROOT}/include")
find_library(CMOCKA_LIBRARY NAMES cmocka HINTS "${CMOCKA_ROOT}/lib" "${CMOCKA_ROOT}/lib64")
if(NOT CMOCKA_INCLUDE_DIR OR NOT CMOCKA_LIBRARY)
    message(FATAL_ERROR "cmocka not found - pass -DCMOCKA_ROOT=<prefix with include/ and lib/> (use the x64 build for a 64-bit gcc, x86 for 32-bit)")
endif()
target_include_directories(run_tests PRIVATE "${CMOCKA_INCLUDE_DIR}")
target_link_libraries(run_tests PRIVATE "${CMOCKA_LIBRARY}")

enable_testing()
add_test(NAME unit_tests COMMAND run_tests)
