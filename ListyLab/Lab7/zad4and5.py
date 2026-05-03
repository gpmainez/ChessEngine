from functools import cache


def make_generator(f):
    def inside_generator(*args, **kwargs):
        arg = 1
        while True:
            yield f(arg, *args, **kwargs)
            arg += 1

    return inside_generator()


def make_generator_mem(f):
    memoized_f = cache(f)
    return make_generator(memoized_f)


def fibonacci(n):
    if n == 0:
        return 0

    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b

    return a


@cache
def fibonacci_memoized(n):
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(4))

fun = make_generator(fibonacci)

for _ in range(10):
    print(next(fun))

seq = make_generator(lambda n: n ** 2)

seqq = make_generator(lambda n: (n + 6) * 7)

for _ in range(10):
    print(next(seq))
    print(next(seqq))
