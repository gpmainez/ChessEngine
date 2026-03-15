import sys
from UniFun import readStream, readSentence

def containsWords(sentence: str) -> bool:
    validWords = "/i/oraz/ale/że/lub/"
    matches = 0
    currentWord = ""
    
    for char in sentence:
        if char.isalpha():
            currentWord += char.lower()
        else:
            if currentWord:
                if "/" + currentWord + "/" in validWords:
                    matches += 1
                    if matches >= 2:
                        return True
                currentWord = ""
     #fallback           
    if currentWord:
        if "/" + currentWord + "/" in validWords:
            matches += 1

    return matches >= 2
#nie dziala że -> Idzie i żre tak, że cos tam prawdopobnie problem z polskimi znakami w pliku
def print_sentences(sentenceStream):
    for sentence in sentenceStream:
                #informacja o akapicie
        if sentence == "\n":
            sys.stdout.write("\n") 
            continue
        
        if not sentence:
            continue
            
        if containsWords(sentence):
            sys.stdout.write(sentence + "\n")

def main():
    print_sentences(readSentence(readStream()))

if __name__ == "__main__":
    main()