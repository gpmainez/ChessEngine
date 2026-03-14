import sys
from UniFun import readStream
def countChars():
    count = 0
    for char in readStream():
        if not char.isspace():
            count += 1
    return count
def main ():
    numChars = countChars()
    print(numChars)

if __name__ == "__main__":
    main()