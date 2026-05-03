def sum_odd(lst,acc = 0):
    return acc if not lst else sum_odd(lst[1:], acc) if lst[0] % 2 == 0 else sum_odd(lst[1:], acc+lst[0])

def get_median(in_lst):

    lst = sorted(in_lst)
    length = len(lst)
    return (
        lambda: (lst[length//2], (lst[length//2] + lst[length//2-1]) / 2)[length % 2 == 0],
        lambda: 0
        )[length == 0]()

def pierwiastek(x, epsilon=0.1, y=1.0):
    return (
        lambda:(
            lambda: pierwiastek(x, epsilon, (y + x / y) / 2),
            lambda: y
        )[abs(y**2 - x) < epsilon](),
        lambda: ValueError("nie mozna pierwiastkowac ujemnej")
    )[x < 0]()



if __name__ == '__main__':
    print(sum_odd([1,2,3,4,-5,2,8]))
    print(sum_odd([]))
    print(sum_odd([2]))

    print("\n\n zadanie b")
    print(get_median([3,2,5,1,4]))
    print(get_median([2,4,3,2]))
    print(get_median([]))
    print(get_median([1]))

    print("\n\n zadanie c")
    print(pierwiastek(-5))
    print(pierwiastek(3))
    print(pierwiastek(0,epsilon=0.0000001))