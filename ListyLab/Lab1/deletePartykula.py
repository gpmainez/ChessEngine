import sys
import io
from UniFun import clean

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def main():
    startBook = False
    prviousLine = False
    inFile = True
    bufor = ""

    while inFile:

        char = sys.stdin.read(1)
        if char == "":
            if startBook and bufor:
                print(clean(bufor))
            inFile = False

        if char == "\n":
            if startBook:
                print(clean(bufor)) if bufor.strip() != "" else print()
            else:
                if bufor.strip() == "" and prviousLine:
                    startBook = True
                prviousLine = (bufor.strip() == "")
            bufor = ""
        else:
            bufor += char




if __name__ == "__main__":
    main()
