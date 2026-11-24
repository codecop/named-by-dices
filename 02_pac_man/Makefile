# POSIX build (Linux/macOS). Windows/MinGW: use Makefile.win. Shared parts: Makefile.common.
include Makefile.common

COV_FLAGS := -std=c99 -Wall -Wextra -Werror -pedantic -O0 -g --coverage
COV_LIB_OBJ := $(patsubst $(SRC_DIR)/%.c,$(COV)/%.o,$(LIB_SRC))
COV_MAIN_OBJ := $(patsubst $(SRC_DIR)/%.c,$(COV)/%.o,$(MAIN_SRC))
COV_TEST_OBJ := $(patsubst $(SRC_DIR)/test/%.c,$(COV)/test_%.o,$(TEST_SRC))

LCOV ?= lcov
GENHTML ?= genhtml

.PHONY: smoke coverage clean

smoke: $(GAME)
	printf 'dq' | $(RUN)$(GAME) > /dev/null
	printf '' | $(RUN)$(GAME) > /dev/null
	python3 $(SRC_DIR)/test/smoke_pty.py $(RUN)$(GAME)

$(COV)/%.o: $(SRC_DIR)/%.c | $(COV)
	$(CC) $(COV_FLAGS) -I$(SRC_DIR) -c $< -o $@

$(COV)/test_%.o: $(SRC_DIR)/test/%.c | $(COV)
	$(CC) $(COV_FLAGS) -I$(SRC_DIR) $(CMOCKA_CFLAGS) -c $< -o $@

$(COV):
	mkdir -p $@

$(COV)/pacman: $(COV_LIB_OBJ) $(COV_MAIN_OBJ) | $(COV)
	$(CC) $(COV_FLAGS) -o $@ $(COV_LIB_OBJ) $(COV_MAIN_OBJ)

$(COV)/run_tests: $(COV_LIB_OBJ) $(COV_TEST_OBJ) | $(COV)
	$(CC) $(COV_FLAGS) -o $@ $(COV_LIB_OBJ) $(COV_TEST_OBJ) $(CMOCKA_LIBS)

coverage: $(COV)/pacman $(COV)/run_tests
	$(RUN)$(COV)/run_tests
	printf 'dq' | $(RUN)$(COV)/pacman > /dev/null
	printf '' | $(RUN)$(COV)/pacman > /dev/null
	python3 $(SRC_DIR)/test/smoke_pty.py $(RUN)$(COV)/pacman
	$(LCOV) --capture --directory $(COV) --output-file $(COV)/coverage.info --rc lcov_branch_coverage=1
	$(GENHTML) --branch-coverage -o docs/coverage-report $(COV)/coverage.info

clean:
	rm -rf $(BUILD) $(COV)
