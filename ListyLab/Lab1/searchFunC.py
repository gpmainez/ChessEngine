import sys
from UniFun import iterate_sentences

def percentOfSent():
    text = sys.stdin.read()
    sentenceCount = 0
    nameSentCount = 0

    for sentence in iterate_sentences(text):
        sentenceCount += 1

        wordNum = 0
        startWord = True
        nameSentBool = False

        for char in sentence:
            if startWord and char.isalpha():
                if wordNum > 0 and char.isupper():
                    nameSentBool = True

                startWord = False
                wordNum += 1

            if char == ' ':
                startWord = True
        if nameSentBool:
                nameSentCount += 1

    if sentenceCount > 0:
        return (nameSentCount/sentenceCount) * 100
    # return None

if __name__ == "__main__":
    result = percentOfSent()
    if result is not None:
        print(result)