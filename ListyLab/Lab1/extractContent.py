import sys
import io
from UniFun import clean, readStream

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
        if char == "\n":
            lineCount += 1
            cleaned = clean(buffer)

            if cleaned[:5] == "-----":
                break

            formattedLine = cleaned + "\n" if cleaned != "" else "\n"

            if not startBook:
                earlyBuffer += formattedLine

                if cleaned == "" and previousLineEmpty:
                    startBook = True
                    earlyBuffer = ""
                elif lineCount >= 10:
                    startBook = True
                    yield earlyBuffer
                    earlyBuffer = ""

                previousLineEmpty = (cleaned == "")
            else:
                yield formattedLine

            buffer = ""
        else:
            buffer += char


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
