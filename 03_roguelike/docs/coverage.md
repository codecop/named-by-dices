# Coverage

Unit tests: `python3 -m unittest discover -s test -t . -p '*_test.py'` (159 tests, plain `unittest`).

Branch coverage via `coverage run -m unittest discover -s test -t . -p '*_test.py'`: **100%** total (1102 statements, 314 branches, 0 missed).

HTML report: [coverage-report/index.html](coverage-report/index.html), regenerate with `coverage html -d docs/coverage-report`.

| File | Coverage |
| ---- | -------- |
| `src/__init__.py` | 100% |
| `src/builder_dummy.py` | 100% |
| `src/builder_service.py` | 100% |
| `src/business_helper.py` | 100% |
| `src/data_common.py` | 100% |
| `src/executor_service.py` | 100% |
| `src/factory_object.py` | 100% |
| `src/helper_data.py` | 100% |
| `src/impl_object.py` | 100% |
| `src/main.py` | 100% |
| `src/manager_common.py` | 100% |
| `src/object_common.py` | 100% |
| `src/processor_utils.py` | 100% |
| `src/service_data.py` | 100% |
| `src/utils_executor.py` | 100% |
| **TOTAL** | **100%** |
