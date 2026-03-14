from UniFun import readStream, readSentence

def isValid(sentence):
    if sentence.count(",") > 1: return True
    return False

def getFirst(sentenceStream):
    for sentence in sentenceStream:
        if isValid(sentence): return sentence

    return "W tekscie nie znaleziono oczekiwanego zdania"

def main():
    sentence = getFirst(readSentence(readStream()))
    print(sentence)

if __name__ == "__main__":
    main()