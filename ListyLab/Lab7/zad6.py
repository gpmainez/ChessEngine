import logging
import time
from functools import wraps
import inspect


logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)

def custom_log(log_level=logging.INFO):
    def decorator(target):
        
        if inspect.isclass(target):
            original_init = target.__init__
            @wraps(original_init)
            def logged_init(self, *args, **kwargs):
                logging.log(
                    log_level,
                    f"[CLASS] Initiantilizing '{target.__name__}' | "
                    f"Args: {args}, Kwargs: {kwargs}"
                )
                original_init(self, *args, **kwargs)
            target.__init__ = logged_init
            return target

        else:
            @wraps(target)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                
                result = target(*args, **kwargs)
                
                duration = time.perf_counter() - start_time
                
                logging.log(
                    log_level,
                    f"[FUNCTION] {target.__name__} | "
                    f"Executed in: {duration:.5f}s | "
                    f"Args: {args}, Kwargs: {kwargs} | "
                    f"Result: {result}"
                )
                return result
            return wrapper
            
    return decorator

def test_6():
    print("\ntestowanie log")

    @custom_log(log_level=logging.DEBUG)
    def multiply_values(a, b, multiplier=1):
        time.sleep(0.01)
        return (a + b) * multiplier

    @custom_log(log_level=logging.DEBUG)
    def flatten_list(seq):
        return [] if not seq else (
            flatten_list(seq[0]) + flatten_list(seq[1:]) if isinstance(seq[0], (list, tuple)) else [seq[0]] + flatten_list(seq[1:])
        )

    @custom_log(log_level=logging.INFO)
    class Student:
        def __init__(self, first_name, last_name, index_number):
            self.first_name = first_name
            self.last_name = last_name
            self.index_number = index_number
            
    print("\ntest dla prostej funkcji")
    res_math = multiply_values(5, 7, multiplier=2)
    
    print("\ntest dla rekurencyjnego flatten z zadania 1")
    res_flat = flatten_list([1, [2, 3]])
    
    print("\nlogowanie na przykladzie klasy student")
    student_1 = Student("Adrian", "Lobster", index_number="643532")
    student_2 = Student("Adrianna", "Lobinho", index_number="532674")
    student_3 = Student("Adisiek","Lobuś","523532")

if __name__ == '__main__':
    test_6()