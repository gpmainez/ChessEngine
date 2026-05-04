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

def make_alpha_dict(text):
    words = "".join(c if c.isalpha() else ' ' for c in text).split()
    return dict(map(lambda c: (c, list(filter(lambda w: c in w, words))), filter(str.isalpha, set(text))))

def flatten(seq):
    return [] if not seq else (flatten(seq[0]) + flatten(seq[1:]) if isinstance(seq[0], (list, tuple)) else [seq[0]] + flatten(seq[1:]))

def group_anagrams(words):
    return {"".join(sorted(w)): [word for word in words if sorted(word) == sorted(w)] for w in words}


def test_a():
    print(sum_odd([1,2,3,4,-5,2,8]))
    print(sum_odd([]))
    print(sum_odd([2]))
def test_b():
    print("\n\n zadanie b")
    print(get_median([3,2,5,1,4]))
    print(get_median([2,4,3,2]))
    print(get_median([]))
    print(get_median([1]))
def test_c():
    print("\n\n zadanie c")
    print(pierwiastek(-5))
    print(pierwiastek(3))
    print(pierwiastek(0,epsilon=0.0000001))

def test_d():
    print("\n zadanie d, alpha dict")
    print("\ntekst z listy")
    print(make_alpha_dict("on i ona"))
    print("\ndluzszy tekst z powtarzajacymi sie literami")
    print(make_alpha_dict("ala i ola mają alergię na ule oraz indyki"))
    print("\npusta lista")
    print(make_alpha_dict(""))
    print("\nfiltrowanie znakow specjalnych, tekst to ala/// t53 35sg;yr")
    print(make_alpha_dict("ala/// t53 35sg;yr"))

def test_e():

    print("\n zadanie e, flatten")
    print("\nlista z listy")
    print(flatten([1, [2, 3], [[4, 5], 6]]))
    
    print("\npusta lista:")
    print(flatten([]))
    
    print("\n zagniezdzenia krotki i listy ze stringami:")
    print(flatten([("a", ["b", ("c", "d")]), [[["e"]]], "f"]))
    
    print("\nlista płaska (brak zmian):")
    print(flatten([1, 2, 3, 4]))

def test_f():
    print("\n zadanie f anagramy")
    print("\nlista z listy:")
    print(group_anagrams(["kot", "tok", "pies", "kep", "pek"]))
    
    print("\npusta lista")
    print(group_anagrams([]))
    
    print("\nlista bez anagramow")
    print(group_anagrams(["jeden", "dwa", "trzy"]))
    
    print("\nanagramy z rozna dl slow:")
    print(group_anagrams(["ula", "lua", "alu", "adrian", "nidraa"]))

if __name__ == '__main__':
    test_f()