import sys


def numOfChars():
    count = 0
    for line in sys.stdin:
        for char in line:
            if char != "\n\t\r":
                count += 1
    print(count)

if __name__ == "__main__":
    numOfChars()