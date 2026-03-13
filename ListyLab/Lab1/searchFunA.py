import sys


def pararg():
    count = 0
    PrevEmptyLine = False
    bufor = ""
    inFile = True

    while inFile:
        char = sys.stdin.read(1)

        if char == "":
            inFile = False  # liczyc ostani wiersz jako akapit?


        if char == "\n":
            if bufor.strip() == "":
                PrevEmptyLine = True
            else:
                if PrevEmptyLine:
                    count += 1
                PrevEmptyLine = False
            bufor = ""
        else:
            bufor += char
    print(count)


if __name__ == "__main__":
    pararg()
