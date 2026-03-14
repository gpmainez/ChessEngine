import sys
from UniFun import read_sentence, read_stream

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

def print_sentences(sentenceStream):
    for sentence in sentenceStream:
        if not sentence:
            continue
            
        if containsWords(sentence):
            sys.stdout.write(sentence + "\n")

def main():
    print_sentences(read_sentence(read_stream()))

if __name__ == "__main__":
    main()