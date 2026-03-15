import sys
from UniFun import readStream


def countPar():
    count = 0
    inParagraph = False
    bufor = ""

    for char in readStream():
        if char == "\n":
            if bufor.strip() != "":
                if inParagraph:
                    count += 1
                    inParagraph = False
            else:
                inParagraph = True

            bufor = ""
        else:
            bufor += char

    #jesli nie endline
    if bufor.strip() != "" and not inParagraph:
        count += 1

    return count

def main():
    result = countPar()
    sys.stdout.write(str(result) + "\n")

if __name__ == "__main__":
    main()