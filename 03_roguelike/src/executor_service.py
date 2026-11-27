import random


def executor_i(data: int, helper: int) -> float:
    return min(0.95, max(0.05, 0.6 + 0.05 * (data - helper)))


def arolla_service(builder: random.Random, data: int, helper: int) -> int:
    if builder.random() >= executor_i(data, helper):
        return 0
    return max(1, builder.randint(1, 6) + data - helper)
