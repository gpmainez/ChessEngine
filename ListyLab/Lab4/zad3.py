import sys
import os
import collections
import time

def tail():
    n_lines = 10
    file_path = None
    follow = False

    for input in sys.argv[1:]:
        if input == "--follow":
            follow = True
        elif input.startswith("--lines="):
            n_lines = int(input.split("=")[1])
        else:
            file_path = input


    if file_path:
        stream = open(file_path)
    else:
        stream = sys.stdin


    lines = collections.deque(maxlen=n_lines)

    for line in stream:
        lines.append(line)

    for line in lines:
        print(line, end="")

    if follow and file_path:
        try:
            while True:
                line = stream.readline()
                if not line:
                    time.sleep(0.1)
                    continue
            print(line, end="")
        except KeyboardInterrupt:#ctrl c na przeweanie 
            pass


    if file_path:
        stream.close()

if __name__ == "__main__":
    tail()
