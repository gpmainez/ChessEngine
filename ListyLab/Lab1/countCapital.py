import sys
from ListyLab.Lab1.UniFun import readSentence, readStream

def hasCapitalWord(sentence):
    wordCount = 0
    inWord = False
    for char in sentence:
        if char.isalpha():
            if not inWord:
                inWord = True
                wordCount +=1

                if char.isupper() and wordCount > 1:
                    return True
        else:
            inWord = False

    return False

def percentOfSentences():
    total = 0
    withCapital = 0
    for sentence in readSentence(readStream()):
        total += 1
        if hasCapitalWord(sentence):
            withCapital += 1
    if total == 0:
        return -1.0
    return (withCapital / total) * 100.0

def main():
    result = percentOfSentences()
    print(result)

if __name__ == "__main__":
    main()