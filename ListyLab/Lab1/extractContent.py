import sys
import io
from UniFun import clean,readStream

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def extract():
    startBook = False
    previousLineEmpty = False
    buffer = ""
    earlyBuffer = ""
    lineCount = 0
    cleaned = ""

    for char in readStream():
        if char =="\n":
            lineCount +=1
            cleaned = clean(buffer)

            if cleaned[:5] == "-----": #informacja o wydawcy - konczymy
                break
            formattedLine = cleaned + "\n" if cleaned != "" else "\n"
            if not startBook: #czesc do preambuly
                earlyBuffer += formattedLine
                if cleaned == "" and previousLineEmpty:
                    startBook = True
                    earlyBuffer = "" #czyscimy, poniewaz wczesniej tu byla preambula
                elif lineCount >= 10:
                    startBook = True
                    yield earlyBuffer #nie wykrylismy preambuly, wiec te pierwsze 10 linii od razu przekazywny
                    earlyBuffer = ""

                previousLineEmpty = (cleaned == "")
            else:
                yield formattedLine #jestesmy w ksiazce - przekazujemy oczyszczona linie

            buffer = ""
        else:           
            buffer += char #proces budowania linii, budujemy az do \n


#zabezpieczenie gdyby na koncu pliku nie bylo \n
    if buffer != "":
        cleaned = clean(buffer)
    if not startBook:
        yield earlyBuffer + cleaned + "\n"
    else:
        yield cleaned + "\n"

def main():
    for line in extract():
        sys.stdout.write(line)

if __name__ == "__main__":
    main()