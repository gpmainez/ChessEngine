import sys
from UniFun import readSentence, readStream


def isValid(sentence):
    if(sentence[-1] in "?!"): return True
    return False

def print_sentences(sentenceStream):
    for sentence in sentenceStream:
        #informacja o akapicie
        if sentence == "\n":
            sys.stdout.write("\n") 
            continue

        if isValid(sentence):
            sys.stdout.write(sentence +"\n")

def main():
    print_sentences(readSentence(readStream()))


if __name__ == "__main__":
    main()
