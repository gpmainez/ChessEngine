import sys

def numOfChars():
    count = 0
    while True:
        char = sys.stdin.read(1)
        if not char:
            break
        if char != " ":
            count += 1
    print(count)

if __name__ == "__main__":
    numOfChars()