import os
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
    try:
        sys.stdout.write(str(num_chars) + "\n")
        sys.stdout.flush()
        os._exit(0)
    except (BrokenPipeError, OSError):
        os._exit(0)

if __name__ == "__main__":
    main()