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
#jedyne co to jak traktowac liczbe w srodku zdania -> firma ma 67 filii extra -- czy 67 to slowo czy nie?
def print_short(sentenceStream):
    for sentence in sentenceStream:
        #informacja o akapicie
        if sentence == "\n":
            sys.stdout.write("\n") 
            continue
        
        if countWords(sentence) <= 4:
            sys.stdout.write(sentence+"\n")

    return ""

def main():
    print_short(readSentence(readStream()))


if __name__ == "__main__":
    main()