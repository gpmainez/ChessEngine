def make_generator(f):
    def inside_generator(*args, **kwargs):
        arg = 1
        while True:
            yield f(arg, *args, **kwargs)
            arg += 1

    return inside_generator()


def fibonacci(n):
    if n == 0:
        return 0

    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b

    return a


print(fibonacci(4))

cwel = make_generator(fibonacci)

for _ in range(10):
    print(next(cwel))

ciagne_druta = make_generator(lambda n: n ** 2)

for _ in range(10):
    print(next(ciagne_druta))