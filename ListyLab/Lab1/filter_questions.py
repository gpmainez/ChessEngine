import sys
from UniFun import read_sentence, read_stream


def is_valid(sentence):
    if not sentence: return False
    if sentence[-1] in "?!": return True
    return False

def print_sentences(sentenceStream):
    for sentence in sentenceStream:
        #informacja o akapicie
        if sentence == "\n":
            sys.stdout.write("\n") 
            continue

        if is_valid(sentence):
            sys.stdout.write(sentence +"\n")


def main():
    print_sentences(read_sentence(read_stream()))


if __name__ == "__main__":
    main()
