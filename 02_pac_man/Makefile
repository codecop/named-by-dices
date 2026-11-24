CC ?= gcc
CFLAGS ?= -std=c99 -Wall -Wextra -Werror -pedantic -O2 -g
CMOCKA_PREFIX ?= /usr
LCOV ?= lcov
GENHTML ?= genhtml

SRC_DIR := src
BUILD := build
COV := build-cov
MAIN_SRC := $(SRC_DIR)/@E@.c
LIB_SRC := $(filter-out $(MAIN_SRC),$(wildcard $(SRC_DIR)/*.c))
TEST_SRC := $(wildcard $(SRC_DIR)/test/*_test.c)

CMOCKA_CFLAGS := -I$(CMOCKA_PREFIX)/include
CMOCKA_LIBS := -L$(CMOCKA_PREFIX)/lib -Wl,-rpath,$(CMOCKA_PREFIX)/lib -lcmocka

GAME := $(BUILD)/pacman
TESTS := $(BUILD)/run_tests

.PHONY: all test smoke coverage clean

all: $(GAME)

$(BUILD) $(COV):
	mkdir -p $@

$(GAME): $(LIB_SRC) $(MAIN_SRC) | $(BUILD)
	$(CC) $(CFLAGS) -I$(SRC_DIR) -o $@ $(LIB_SRC) $(MAIN_SRC)

$(TESTS): $(LIB_SRC) $(TEST_SRC) | $(BUILD)
	$(CC) $(CFLAGS) -I$(SRC_DIR) $(CMOCKA_CFLAGS) -o $@ $(LIB_SRC) $(TEST_SRC) $(CMOCKA_LIBS)

test: $(TESTS)
	./$(TESTS)

smoke: $(GAME)
	printf 'dq' | ./$(GAME) > /dev/null
	python3 $(SRC_DIR)/test/smoke_pty.py ./$(GAME)

COV_FLAGS := -std=c99 -Wall -Wextra -Werror -pedantic -O0 -g --coverage
COV_LIB_OBJ := $(patsubst $(SRC_DIR)/%.c,$(COV)/%.o,$(LIB_SRC))
COV_MAIN_OBJ := $(patsubst $(SRC_DIR)/%.c,$(COV)/%.o,$(MAIN_SRC))
COV_TEST_OBJ := $(patsubst $(SRC_DIR)/test/%.c,$(COV)/test_%.o,$(TEST_SRC))

$(COV)/%.o: $(SRC_DIR)/%.c | $(COV)
	$(CC) $(COV_FLAGS) -I$(SRC_DIR) -c $< -o $@

$(COV)/test_%.o: $(SRC_DIR)/test/%.c | $(COV)
	$(CC) $(COV_FLAGS) -I$(SRC_DIR) $(CMOCKA_CFLAGS) -c $< -o $@

$(COV)/pacman: $(COV_LIB_OBJ) $(COV_MAIN_OBJ) | $(COV)
	$(CC) $(COV_FLAGS) -o $@ $(COV_LIB_OBJ) $(COV_MAIN_OBJ)

$(COV)/run_tests: $(COV_LIB_OBJ) $(COV_TEST_OBJ) | $(COV)
	$(CC) $(COV_FLAGS) -o $@ $(COV_LIB_OBJ) $(COV_TEST_OBJ) $(CMOCKA_LIBS)

coverage: $(COV)/pacman $(COV)/run_tests
	./$(COV)/run_tests
	printf 'dq' | ./$(COV)/pacman > /dev/null
	python3 $(SRC_DIR)/test/smoke_pty.py ./$(COV)/pacman
	$(LCOV) --capture --directory $(COV) --output-file $(COV)/coverage.info --rc lcov_branch_coverage=1
	$(GENHTML) --branch-coverage -o docs/coverage-report $(COV)/coverage.info

clean:
	rm -rf $(BUILD) $(COV)
