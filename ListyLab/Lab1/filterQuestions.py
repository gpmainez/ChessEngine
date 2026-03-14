import sys
from UniFun import readSentence, readStream


def isValid(sentence):
    if(sentence.last() in "?!"): return True
    return False

def print_sentences(sentenceStream):
    for sentence in sentenceStream:
        if isValid(sentence):
            sys.stdout.write(sentence)

def main():
    print_sentences(readSentence(readStream()))


if __name__ == "__main__":
    main()
