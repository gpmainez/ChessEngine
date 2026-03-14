
import sys

from UniFun import readSentence, readStream


def print_sentences(sentenceStream):
    count = 0
    for sentence in sentenceStream:
        #informacja o akapicie
        if sentence == "\n":
            sys.stdout.write("\n") 
            continue

        if count >= 20: break
        sys.stdout.write(sentence + "\n")
        count += 1

def main():
    print_sentences(readSentence(readStream()))


if __name__ == "__main__":
    main()
