import pytest
from functools import cache


def make_generator(f, *args, **kwargs):
    def inside_generator():
        arg = 0
        while True:
            yield f(arg, *args, **kwargs)
            arg += 1

    return inside_generator()


def make_generator_mem(f, *args, **kwargs):
    memoized_f = cache(f)
    return make_generator(memoized_f, *args, **kwargs)


def fibonacci(n):
    if n == 0:
        return 0
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@cache
def fibonacci_memoized(n):
    if n == 0:
        return 0
    if n <= 2:
        return 1
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def test_fibonacci_sequence_start_at_zero():
    gen = make_generator(fibonacci)
    results = [next(gen) for _ in range(5)]
    assert results == [0, 1, 1, 2, 3]


def test_generator_independence():
    f = lambda n: n
    gen1 = make_generator(f)
    gen2 = make_generator(f)

    assert next(gen1) == 0
    assert next(gen1) == 1
    assert next(gen2) == 0


def test_argument_passing():
    f = lambda n, offset: n + offset
    gen = make_generator(f, offset=10)
    assert next(gen) == 10
    assert next(gen) == 11


def test_memoization_effectiveness():
    call_count = 0

    def spy_function(n):
        nonlocal call_count
        call_count += 1
        return n

    gen_mem = make_generator_mem(spy_function)

    assert next(gen_mem) == 0
    assert call_count == 1

    assert call_count == 1


def test_power_sequence():

    seq = make_generator(lambda n: n ** 2)
    results = [next(seq) for _ in range(4)]
    assert results == [0, 1, 4, 9]



if __name__ == "__main__":
    print("Ciąg Fibonacciego (10 elementów):")
    fun = make_generator(fibonacci)
    for _ in range(10):
        print(next(fun), end=" ")
    print("\n")
