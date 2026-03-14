
import sys

from ListyLab.Lab1.UniFun import readSentence, readStream


def print_sentences(sentenceStream):
    for sentence in sentenceStream in range(20):
        sys.stdout.write(sentence)

def main():
    print_sentences(readSentence(readStream()))


if __name__ == "__main__":
    main()
