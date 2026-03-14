import sys
from UniFun import readSentence, readStream

def countWords(sentence: str) -> int:
    wordCount = 0
    inWord = False
    
    for char in sentence:
        if char.isalpha():
            if not inWord:
                inWord = True
                wordCount += 1
        else:
            inWord = False
            
    return wordCount

def print_short(sentenceStream):
    for sentence in sentenceStream:
        if countWords(sentence) <= 4:
            sys.stdout.write(sentence)

    return "W tekscie nie znaleziono oczekiwanego zdania"

def main():
    print_short(readSentence(readStream()))


if __name__ == "__main__":
    main()