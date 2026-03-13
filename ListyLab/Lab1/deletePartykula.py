

import sys
import io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

def clean(line):
    return " ".join(line.strip().split())

def main():
    lines = sys.stdin.readlines()
    start = 0

    for i in range(min(10, len(lines)-1)):

        if lines[i].strip() == "" and lines[i+1].strip() == "":
            start = i + 2
            break

    for line in lines[start:]:
        if line.strip() == "":
            print()
        else:
            print(clean(line))

if __name__ == "__main__":
    main()



