import sys
from UniFun import readStream

def countPar():
    count = 0
    PrevEmptyLine = False
    bufor = ""

    for char in readStream():
        if char == "\n":
            if bufor.strip() == "":
                if PrevEmptyLine:
                    count += 1
                PrevEmptyLine = True
            else:
                PrevEmptyLine = False
            bufor = ""
        else:
            bufor += char


if __name__ == "__main__":
    countPar()
