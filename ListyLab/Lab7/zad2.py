def forall(pred, iterable):
    return all(map(pred, iterable))

def exists(pred, iterable):
    return any(map(pred, iterable))

def atleast(n, pred, iterable):
    matches = 0
    for element in iterable:
        if pred(element):
            matches += 1
            if matches >= n:
                return True
    return False

def atmost(n, pred, iterable):
    matches = 0
    for element in iterable:
        if pred(element):
            matches += 1
            if matches > n:
                return False
    return True
#do atleast i atmost mozna bylo uzyc sum(map(pred,it)) i porownac z n, ale wtedy nie bylismy zabezpieczeni na nieskonczone generatory

def test_2():
    pred1 = lambda x: x**2 < x
    print("pusta lista []")
    print(f"forall = {forall(pred1,[])}")
    print(f"exists = {exists(pred1,[])}")
    print(f"atleast = {atleast(10,pred1,[])}")
    print(f"atmost = {atmost(10,pred1,[])}")
    
    print("\n liczby od -10 do 20")
    print(f"forall = {forall(pred1,[2,-4,0.75,0.01,5,-2,9,1,11,19,-14])}")
    print(f"exists = {exists(pred1,[2,-4,0.75,0.01,5,-2,9,1,11,19,-14])}")
    print(f"atleast = {atleast(10,pred1,[2,-4,0.75,0.01,5,-2,9,1,11,19,-14])}")
    print(f"atmost = {atmost(10,pred1,[2,-4,0.75,0.01,5,-2,9,1,11,19,-14])}")   

    print("test dla stringow i predykatu isupper")
    is_upper = lambda c: c.isupper()

    text1 = "hello world"
    text2 = "Welcome Golden" 

    print(f"\ntekst1: {text1}")
    print(f"forall = {forall(is_upper, text1)}")
    print(f"exists = {exists(is_upper, text1)}")
    print(f"atleast 1 = {atleast(1, is_upper, text1)}")
    print(f"atmost 0= {atmost(0, is_upper, text1)}")

    print(f"\ntekst2: {text2}")
    print(f"forall = {forall(is_upper, text2)}")
    print(f"exists = {exists(is_upper, text2)}")
    print(f"atleast 1 = {atleast(1, is_upper, text2)}")
    print(f"atmost 2 = {atmost(2, is_upper, text2)}")

    print("\ntest dla nieskonczonego")
    def infinite_numbers():
        i = 1
        while True:
            yield i
            i += 1

    print(f"exists x > 0 = {exists(lambda x: x > 0, infinite_numbers())}")
    
    print(f"forall x < 5 = {forall(lambda x: x < 5, infinite_numbers())}")

    print(f"atleast 3 (x % 2 == 0 = {atleast(3, lambda x: x % 2 == 0, infinite_numbers())}")
    print(f"atmost 3 (x % 3 == 0)= {atmost(3, lambda x: x % 3 == 0, infinite_numbers())}")

if __name__ == '__main__':
    test_2()