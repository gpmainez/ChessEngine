import sys
from uni_fun import read_stream
def count_chars():
    count = 0
    for char in read_stream():
        if not char.isspace():
            count += 1
    return count

def main ():
    num_chars = count_chars()
    print(num_chars)

if __name__ == "__main__":
    main()