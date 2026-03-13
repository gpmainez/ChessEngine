import sys

def percentOfSent():
    sentence_buf = ""
    prevChar = ""
    sentenceCount = 0
    nameSentCount = 0
    wordNum = 0
    startWord = True
    nameSentBool = False
    inFile = True

    while inFile:

        char = sys.stdin.read(1)
        if not char:  # EOF
            if sentence_buf.strip():
                sentenceCount += 1
                if nameSentBool:
                    nameSentCount += 1
            inFile = False

        sentence_buf += char


        if startWord and char.isalpha():
            if wordNum > 0 and char.isupper():
                nameSentBool = True
            startWord = False
            wordNum += 1

        if char in " \t\n":
            startWord = True

        if char in ".!?":
            sentenceCount += 1
            if nameSentBool:
                nameSentCount += 1
            sentence_buf = ""
            startWord = True
            wordNum = 0
            nameSentBool = False

        elif char == "\n" and prevChar == "\n":
            sentenceCount += 1
            if nameSentBool:
                nameSentCount += 1
            sentence_buf = ""
            startWord = True
            wordNum = 0
            nameSentBool = False

        prevChar = char

    if sentenceCount > 0:
        return (nameSentCount / sentenceCount) * 100
    return None


if __name__ == "__main__":
    result = percentOfSent()
    if result is not None:
        print(result)
