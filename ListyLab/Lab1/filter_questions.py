import sys
import os
from uni_fun import read_sentence, read_stream


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
    try: 
        print_sentences(read_sentence(read_stream()))
        sys.stdout.flush()
        os._exit(0)
    except (BrokenPipeError, OSError):
        os._exit(0)

if __name__ == "__main__":
    main()
