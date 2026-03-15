from UniFun import readStream, readSentence

def isValid(sentence):
    if sentence.count(",") > 1: return True #nie wystarczy imo
    return False

def getFirst(sentenceStream):
    for sentence in sentenceStream:
        if isValid(sentence): return sentence

    return ""
#liczysz chyba przecinki czyli wyliczanie blednie ci zaznaczy jakko zdanie podzredne np
#firma to ula, Ola. -> zwroci a to nie ma zdanai podrzednego chyba ze nie ogarniam
#tak samo gdy przecinek to separator liczb 10 np 67,67

def main():
    sentence = getFirst(readSentence(readStream()))
    print(sentence)

if __name__ == "__main__":
    main()